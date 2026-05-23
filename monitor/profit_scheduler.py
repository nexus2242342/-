import threading
import time
import logging
from datetime import datetime, timezone

from config import config, STAKING_PLANS, TRADERS
import db.database as db

logger = logging.getLogger(__name__)

_notify_profit_fn = None


def set_profit_notifier(fn):
    global _notify_profit_fn
    _notify_profit_fn = fn


def _seconds_until_midnight_utc() -> float:
    now = datetime.now(timezone.utc)
    tomorrow = now.replace(hour=0, minute=0, second=0, microsecond=0)
    delta = (tomorrow - now).total_seconds()
    if delta <= 0:
        delta += 86400
    return delta


def _get_plan(plan_id: int) -> dict | None:
    return next((p for p in STAKING_PLANS if p["id"] == plan_id), None)


def _get_trader(trader_id: str) -> dict | None:
    return next((tr for tr in TRADERS if tr["id"] == trader_id), None)


def _run_daily_profit():
    while True:
        wait = _seconds_until_midnight_utc()
        logger.info(f"[PROFIT] Next accrual in {wait:.0f}s ({wait/3600:.1f}h)")
        time.sleep(wait)

        logger.info("[PROFIT] Accruing daily profit for all users…")
        users = db.get_all_users()
        base_pct = config.DAILY_PROFIT_PCT / 100

        for user in users:
            tg_id = user["tg_id"]
            profit_usdt = 0.0
            profit_ton  = 0.0

            # 1. Base balance profit (free balance, not in staking/copy)
            free_usdt = max(0.0, user["balance_usdt"] - user.get("staked_usdt", 0))
            profit_usdt += round(free_usdt * base_pct, 6)
            profit_ton  += round(user["balance_ton"] * base_pct, 6)

            # 2. Staking profit
            staking_positions = db.get_user_staking(tg_id)
            for pos in staking_positions:
                plan_pct = pos["daily_pct"] / 100
                s_profit = round(pos["amount"] * plan_pct, 6)
                profit_usdt += s_profit
                # Update total_earned on staking position
                with db.get_conn() as c:
                    c.execute(
                        "UPDATE staking_positions SET total_earned = total_earned + ? WHERE id = ?",
                        (s_profit, pos["id"])
                    )

            # 3. Copy trading profit
            copy_positions = db.get_user_copy_positions(tg_id)
            for pos in copy_positions:
                trader = _get_trader(pos["trader_id"])
                if not trader:
                    continue
                daily_pct = trader["monthly"] / 30 / 100
                c_profit = round(pos["amount"] * daily_pct, 6)
                profit_usdt += c_profit
                with db.get_conn() as c:
                    c.execute(
                        "UPDATE copy_positions SET total_earned = total_earned + ? WHERE id = ?",
                        (c_profit, pos["id"])
                    )

            if profit_usdt == 0 and profit_ton == 0:
                continue

            db.credit_profit(tg_id, profit_usdt, profit_ton)
            logger.info(
                f"[PROFIT] User {tg_id}: +{profit_usdt:.6f} USDT, +{profit_ton:.6f} TON"
            )

            if _notify_profit_fn:
                updated = db.get_user(tg_id)
                _notify_profit_fn(
                    user_id=tg_id,
                    profit_usdt=profit_usdt,
                    profit_ton=profit_ton,
                    balance_usdt=updated["balance_usdt"] if updated else 0,
                    balance_ton=updated["balance_ton"] if updated else 0,
                    lang=user.get("language", "ru"),
                )

        time.sleep(60)


def start_profit_scheduler():
    t = threading.Thread(target=_run_daily_profit, daemon=True, name="ProfitScheduler")
    t.start()
    logger.info("[PROFIT] Scheduler started.")
