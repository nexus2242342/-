import threading
import time
import logging
from typing import Optional

import requests

from config import config
import db.database as db

logger = logging.getLogger(__name__)

_notify_user_fn  = None
_notify_admin_fn = None


def set_notifiers(notify_user, notify_admin):
    global _notify_user_fn, _notify_admin_fn
    _notify_user_fn  = notify_user
    _notify_admin_fn = notify_admin


class WalletMonitor:
    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(
            target=self._monitor_loop,
            daemon=True,
            name="WalletMonitor"
        )
        self._thread.start()
        logger.info("[MONITOR] Started.")

    def stop(self):
        self.running = False
        if self._thread:
            self._thread.join(timeout=10)

    def _monitor_loop(self):
        while self.running:
            try:
                logger.info("[MONITOR] Checking TON wallet…")
                self._check_ton_wallet()
            except Exception as e:
                logger.error(f"[MONITOR] TON check error: {e}")
            try:
                logger.info("[MONITOR] Checking USDT wallet…")
                self._check_usdt_wallet()
            except Exception as e:
                logger.error(f"[MONITOR] USDT check error: {e}")
            logger.info(f"[MONITOR] Next check in {config.CHECK_INTERVAL}s")
            time.sleep(config.CHECK_INTERVAL)

    # ─── TON ──────────────────────────────────────────────
    def _check_ton_wallet(self):
        url = f"{config.TON_API_URL}/getTransactions"
        params = {"address": config.TON_WALLET, "limit": config.TX_SCAN_LIMIT}
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        transactions = resp.json().get("result", [])
        logger.info(f"[MONITOR] TON: fetched {len(transactions)} txs")

        for tx in transactions:
            tx_hash = tx.get("transaction_id", {}).get("hash", "")
            if not tx_hash or db.is_tx_processed(tx_hash):
                continue
            in_msg = tx.get("in_msg", {})
            raw_value = in_msg.get("value")
            if not raw_value:
                continue
            amount    = int(raw_value) / 1e9
            from_addr = in_msg.get("source", "unknown")
            timestamp = tx.get("utime", int(time.time()))
            comment   = in_msg.get("message", "")

            if amount < config.MIN_DEPOSIT_TON:
                continue

            user_id = self._resolve_user(comment, amount, "TON", timestamp)
            db.save_processed_tx(tx_hash, user_id or 0, amount, "TON")

            if user_id:
                db.credit_deposit(user_id, amount, "TON")
                user = db.get_user(user_id)
                if user and _notify_user_fn:
                    _notify_user_fn(
                        user_id, amount, "TON", tx_hash,
                        user["balance_usdt"], user["balance_ton"],
                        user.get("language", "ru"),
                    )
                if _notify_admin_fn:
                    _notify_admin_fn(user_id, user["username"] if user else None,
                                     amount, "TON", tx_hash)
                self._process_referral(user_id, amount, "TON")
            else:
                if _notify_admin_fn:
                    _notify_admin_fn(None, None, amount, "TON", tx_hash,
                                     unidentified=True, from_addr=from_addr)

    # ─── USDT (TRC-20) ────────────────────────────────────
    def _check_usdt_wallet(self):
        url = f"{config.TRON_API_URL}/accounts/{config.USDT_WALLET}/transactions/trc20"
        params = {
            "limit": config.TX_SCAN_LIMIT,
            "contract_address": config.USDT_CONTRACT,
            "only_to": True,
        }
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        transactions = resp.json().get("data", [])
        logger.info(f"[MONITOR] USDT: fetched {len(transactions)} txs")

        for tx in transactions:
            tx_hash = tx.get("transaction_id", "")
            if not tx_hash or db.is_tx_processed(tx_hash):
                continue
            try:
                amount = int(tx.get("value", 0)) / 1e6
            except (ValueError, TypeError):
                continue
            from_addr = tx.get("from", "unknown")
            timestamp = tx.get("block_timestamp", int(time.time()) * 1000) // 1000

            if amount < config.MIN_DEPOSIT_USDT:
                continue

            user_id = self._resolve_user("", amount, "USDT", timestamp)
            db.save_processed_tx(tx_hash, user_id or 0, amount, "USDT")

            if user_id:
                db.credit_deposit(user_id, amount, "USDT")
                user = db.get_user(user_id)
                if user and _notify_user_fn:
                    _notify_user_fn(
                        user_id, amount, "USDT", tx_hash,
                        user["balance_usdt"], user["balance_ton"],
                        user.get("language", "ru"),
                    )
                if _notify_admin_fn:
                    _notify_admin_fn(user_id, user["username"] if user else None,
                                     amount, "USDT", tx_hash)
                self._process_referral(user_id, amount, "USDT")
            else:
                if _notify_admin_fn:
                    _notify_admin_fn(None, None, amount, "USDT", tx_hash,
                                     unidentified=True, from_addr=from_addr)

    # ─── Helpers ──────────────────────────────────────────
    def _resolve_user(self, comment: str, amount: float,
                      currency: str, timestamp: int) -> Optional[int]:
        if comment.startswith("DEPOSIT_"):
            try:
                uid = int(comment.split("_")[1])
                if db.get_user(uid):
                    logger.info(f"[MONITOR] Resolved via comment → user {uid}")
                    return uid
            except (IndexError, ValueError):
                pass

        pending = db.find_pending_by_amount(amount, currency, timestamp)
        if pending:
            db.mark_pending_done(pending["id"])
            logger.info(f"[MONITOR] Resolved via pending → user {pending['user_id']}")
            return pending["user_id"]
        return None

    def _process_referral(self, user_id: int, amount: float, currency: str):
        """Give referral bonus on first deposit."""
        user = db.get_user(user_id)
        if not user or not user.get("referred_by"):
            return
        # Only if this is first deposit
        from db.database import count_user_operations
        ops = count_user_operations(user_id)
        if ops != 1:  # first deposit creates exactly 1 operation
            return
        bonus_pct = config.REFERRAL_BONUS_PCT / 100
        bonus_usdt = 0.0
        if currency == "USDT":
            bonus_usdt = round(amount * bonus_pct, 4)
        elif currency == "TON":
            # approximate: convert TON→USDT at rough rate 5$
            bonus_usdt = round(amount * 5 * bonus_pct, 4)
        if bonus_usdt > 0:
            db.add_referral_bonus(user["referred_by"], bonus_usdt)
            logger.info(f"[REFERRAL] +{bonus_usdt} USDT to user {user['referred_by']}")


monitor = WalletMonitor()
