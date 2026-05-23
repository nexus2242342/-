import sqlite3
import time
import hashlib
import logging
from contextlib import contextmanager
from typing import Optional, List, Dict, Any

from config import config

logger = logging.getLogger(__name__)


@contextmanager
def get_conn():
    conn = sqlite3.connect(config.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _ref_code(tg_id: int) -> str:
    h = hashlib.md5(str(tg_id).encode()).hexdigest()[:6].upper()
    return f"CP{h}"


def init_db():
    with get_conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            tg_id             INTEGER PRIMARY KEY,
            username          TEXT,
            language          TEXT    DEFAULT 'ru',
            referral_code     TEXT    UNIQUE,
            referred_by       INTEGER,
            balance_usdt      REAL    DEFAULT 0,
            balance_ton       REAL    DEFAULT 0,
            deposited_usdt    REAL    DEFAULT 0,
            deposited_ton     REAL    DEFAULT 0,
            staked_usdt       REAL    DEFAULT 0,
            referral_earnings REAL    DEFAULT 0,
            created_at        INTEGER,
            last_active       INTEGER
        );

        CREATE TABLE IF NOT EXISTS processed_transactions (
            tx_hash      TEXT    PRIMARY KEY,
            user_id      INTEGER,
            amount       REAL,
            currency     TEXT,
            processed_at INTEGER
        );

        CREATE TABLE IF NOT EXISTS withdraw_requests (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            amount      REAL,
            currency    TEXT,
            address     TEXT,
            status      TEXT DEFAULT 'pending',
            created_at  INTEGER
        );

        CREATE TABLE IF NOT EXISTS pending_deposits (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER,
            amount     REAL,
            currency   TEXT,
            timestamp  INTEGER,
            status     TEXT DEFAULT 'pending'
        );

        CREATE TABLE IF NOT EXISTS profit_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            amount_usdt REAL DEFAULT 0,
            amount_ton  REAL DEFAULT 0,
            source      TEXT DEFAULT 'trading',
            created_at  INTEGER
        );

        CREATE TABLE IF NOT EXISTS staking_positions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER,
            plan_id      INTEGER,
            amount       REAL,
            daily_pct    REAL,
            lock_days    INTEGER,
            started_at   INTEGER,
            unlock_at    INTEGER,
            status       TEXT DEFAULT 'active',
            total_earned REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS referrals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_id INTEGER,
            bonus_paid  REAL  DEFAULT 0,
            created_at  INTEGER
        );

        CREATE TABLE IF NOT EXISTS copy_positions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            trader_id   TEXT,
            amount      REAL,
            currency    TEXT DEFAULT 'USDT',
            started_at  INTEGER,
            status      TEXT DEFAULT 'active',
            total_earned REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS operations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            op_type     TEXT,
            amount      REAL,
            currency    TEXT,
            description TEXT,
            created_at  INTEGER
        );
        """)
    logger.info("DB initialised.")


# ─────────────────────────── USERS ───────────────────────────

def upsert_user(tg_id: int, username: Optional[str], referred_by_code: str = None):
    now = int(time.time())
    ref_code = _ref_code(tg_id)
    with get_conn() as c:
        c.execute("""
            INSERT INTO users (tg_id, username, referral_code, created_at, last_active)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(tg_id) DO UPDATE SET
                username    = excluded.username,
                last_active = excluded.last_active
        """, (tg_id, username, ref_code, now, now))

        if referred_by_code:
            row = c.execute(
                "SELECT tg_id FROM users WHERE referral_code = ?", (referred_by_code,)
            ).fetchone()
            if row and row["tg_id"] != tg_id:
                c.execute("""
                    UPDATE users SET referred_by = ?
                    WHERE tg_id = ? AND referred_by IS NULL
                """, (row["tg_id"], tg_id))
                c.execute("""
                    INSERT OR IGNORE INTO referrals (referrer_id, referred_id, created_at)
                    VALUES (?, ?, ?)
                """, (row["tg_id"], tg_id, now))


def get_user(tg_id: int) -> Optional[Dict]:
    with get_conn() as c:
        r = c.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,)).fetchone()
        return dict(r) if r else None


def get_all_users() -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute("SELECT * FROM users").fetchall()]


def set_language(tg_id: int, lang: str):
    with get_conn() as c:
        c.execute("UPDATE users SET language = ? WHERE tg_id = ?", (lang, tg_id))


def credit_deposit(tg_id: int, amount: float, currency: str):
    now = int(time.time())
    with get_conn() as c:
        if currency == "USDT":
            c.execute("""UPDATE users SET balance_usdt = balance_usdt + ?,
                         deposited_usdt = deposited_usdt + ? WHERE tg_id = ?""",
                      (amount, amount, tg_id))
        else:
            c.execute("""UPDATE users SET balance_ton = balance_ton + ?,
                         deposited_ton = deposited_ton + ? WHERE tg_id = ?""",
                      (amount, amount, tg_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'deposit', ?, ?, 'Deposit', ?)""",
                  (tg_id, amount, currency, now))


def credit_profit(tg_id: int, usdt: float, ton: float, source: str = "trading"):
    now = int(time.time())
    with get_conn() as c:
        c.execute("""UPDATE users SET balance_usdt = balance_usdt + ?,
                     balance_ton = balance_ton + ? WHERE tg_id = ?""",
                  (usdt, ton, tg_id))
        c.execute("""INSERT INTO profit_log (user_id, amount_usdt, amount_ton, source, created_at)
                     VALUES (?, ?, ?, ?, ?)""", (tg_id, usdt, ton, source, now))
        if usdt > 0:
            c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                         VALUES (?, 'profit', ?, 'USDT', ?, ?)""",
                      (tg_id, usdt, f"Profit ({source})", now))
        if ton > 0:
            c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                         VALUES (?, 'profit', ?, 'TON', ?, ?)""",
                      (tg_id, ton, f"Profit ({source})", now))


def debit_balance(tg_id: int, amount: float, currency: str):
    now = int(time.time())
    with get_conn() as c:
        if currency == "USDT":
            c.execute("UPDATE users SET balance_usdt = balance_usdt - ? WHERE tg_id = ?", (amount, tg_id))
        else:
            c.execute("UPDATE users SET balance_ton = balance_ton - ? WHERE tg_id = ?", (amount, tg_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'withdraw', ?, ?, 'Withdrawal', ?)""",
                  (tg_id, amount, currency, now))


# ─────────────────────────── TRANSACTIONS ─────────────────────────

def is_tx_processed(tx_hash: str) -> bool:
    with get_conn() as c:
        return c.execute(
            "SELECT 1 FROM processed_transactions WHERE tx_hash = ?", (tx_hash,)
        ).fetchone() is not None


def save_processed_tx(tx_hash: str, user_id: int, amount: float, currency: str):
    now = int(time.time())
    with get_conn() as c:
        c.execute("""
            INSERT OR IGNORE INTO processed_transactions (tx_hash, user_id, amount, currency, processed_at)
            VALUES (?, ?, ?, ?, ?)
        """, (tx_hash, user_id, amount, currency, now))


# ─────────────────────────── PENDING DEPOSITS ─────────────────────────

def add_pending_deposit(user_id: int, amount: float, currency: str):
    now = int(time.time())
    with get_conn() as c:
        c.execute("""
            INSERT INTO pending_deposits (user_id, amount, currency, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, amount, currency, now))


def find_pending_by_amount(amount: float, currency: str, ts: int) -> Optional[Dict]:
    with get_conn() as c:
        r = c.execute("""
            SELECT * FROM pending_deposits
            WHERE currency = ? AND status = 'pending'
              AND ABS(amount - ?) < 0.01
              AND ABS(timestamp - ?) < 300
            ORDER BY timestamp DESC LIMIT 1
        """, (currency, amount, ts)).fetchone()
        return dict(r) if r else None


def mark_pending_done(pending_id: int):
    with get_conn() as c:
        c.execute("UPDATE pending_deposits SET status = 'done' WHERE id = ?", (pending_id,))


# ─────────────────────────── WITHDRAWALS ─────────────────────────

def create_withdraw(user_id: int, amount: float, currency: str, address: str) -> int:
    now = int(time.time())
    with get_conn() as c:
        cur = c.execute("""
            INSERT INTO withdraw_requests (user_id, amount, currency, address, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, amount, currency, address, now))
        return cur.lastrowid


def get_pending_withdrawals() -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM withdraw_requests WHERE status = 'pending' ORDER BY created_at DESC"
        ).fetchall()]


def get_withdraw_by_id(wid: int) -> Optional[Dict]:
    with get_conn() as c:
        r = c.execute("SELECT * FROM withdraw_requests WHERE id = ?", (wid,)).fetchone()
        return dict(r) if r else None


def update_withdraw_status(wid: int, status: str):
    with get_conn() as c:
        c.execute("UPDATE withdraw_requests SET status = ? WHERE id = ?", (status, wid))


# ─────────────────────────── STAKING ─────────────────────────

def create_staking(user_id: int, plan_id: int, amount: float, daily_pct: float, lock_days: int) -> int:
    now = int(time.time())
    unlock_at = now + lock_days * 86400 if lock_days > 0 else 0
    with get_conn() as c:
        cur = c.execute("""
            INSERT INTO staking_positions (user_id, plan_id, amount, daily_pct, lock_days, started_at, unlock_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, plan_id, amount, daily_pct, lock_days, now, unlock_at))
        c.execute("""UPDATE users SET balance_usdt = balance_usdt - ?,
                     staked_usdt = staked_usdt + ? WHERE tg_id = ?""",
                  (amount, amount, user_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'staking_open', ?, 'USDT', 'Staking opened', ?)""",
                  (user_id, amount, now))
        return cur.lastrowid


def get_user_staking(user_id: int) -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM staking_positions WHERE user_id = ? AND status = 'active' ORDER BY started_at DESC",
            (user_id,)
        ).fetchall()]


def close_staking(pos_id: int, user_id: int, amount: float, earned: float):
    now = int(time.time())
    with get_conn() as c:
        c.execute("UPDATE staking_positions SET status = 'closed' WHERE id = ?", (pos_id,))
        c.execute("""UPDATE users SET balance_usdt = balance_usdt + ?,
                     staked_usdt = staked_usdt - ? WHERE tg_id = ?""",
                  (amount + earned, amount, user_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'staking_close', ?, 'USDT', 'Staking closed + profit', ?)""",
                  (user_id, amount + earned, now))


# ─────────────────────────── COPY TRADING ─────────────────────────

def create_copy_position(user_id: int, trader_id: str, amount: float) -> int:
    now = int(time.time())
    with get_conn() as c:
        cur = c.execute("""
            INSERT INTO copy_positions (user_id, trader_id, amount, started_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, trader_id, amount, now))
        c.execute("UPDATE users SET balance_usdt = balance_usdt - ? WHERE tg_id = ?",
                  (amount, user_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'copy_open', ?, 'USDT', ?, ?)""",
                  (user_id, amount, f"Copy trading: {trader_id}", now))
        return cur.lastrowid


def get_user_copy_positions(user_id: int) -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM copy_positions WHERE user_id = ? AND status = 'active' ORDER BY started_at DESC",
            (user_id,)
        ).fetchall()]


def close_copy_position(pos_id: int, user_id: int, amount: float, earned: float):
    now = int(time.time())
    with get_conn() as c:
        c.execute("UPDATE copy_positions SET status = 'closed', total_earned = ? WHERE id = ?",
                  (earned, pos_id))
        c.execute("UPDATE users SET balance_usdt = balance_usdt + ? WHERE tg_id = ?",
                  (amount + earned, user_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'copy_close', ?, 'USDT', 'Copy trading closed + profit', ?)""",
                  (user_id, amount + earned, now))


# ─────────────────────────── REFERRALS ─────────────────────────

def get_user_referrals(user_id: int) -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute(
            "SELECT * FROM referrals WHERE referrer_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()]


def add_referral_bonus(referrer_id: int, amount: float):
    now = int(time.time())
    with get_conn() as c:
        c.execute("""UPDATE users SET balance_usdt = balance_usdt + ?,
                     referral_earnings = referral_earnings + ? WHERE tg_id = ?""",
                  (amount, amount, referrer_id))
        c.execute("""INSERT INTO operations (user_id, op_type, amount, currency, description, created_at)
                     VALUES (?, 'referral_bonus', ?, 'USDT', 'Referral bonus', ?)""",
                  (referrer_id, amount, now))


# ─────────────────────────── HISTORY ─────────────────────────

def get_user_operations(user_id: int, limit: int = 20, offset: int = 0) -> List[Dict]:
    with get_conn() as c:
        return [dict(r) for r in c.execute(
            """SELECT * FROM operations WHERE user_id = ?
               ORDER BY created_at DESC LIMIT ? OFFSET ?""",
            (user_id, limit, offset)
        ).fetchall()]


def count_user_operations(user_id: int) -> int:
    with get_conn() as c:
        r = c.execute("SELECT COUNT(*) as cnt FROM operations WHERE user_id = ?", (user_id,)).fetchone()
        return r["cnt"] if r else 0
