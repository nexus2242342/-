import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
import db.database as db
from handlers import user as user_handlers
from handlers import admin as admin_handlers
from monitor.wallet_monitor import monitor, set_notifiers
from monitor.profit_scheduler import start_profit_scheduler, set_profit_notifier
from utils.messages import fmt_deposit_credited, fmt_profit_notification

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

_bot: Bot = None


# ─── Monitor notification callbacks ──────────────────────
def notify_user(user_id, amount, currency, tx_hash,
                balance_usdt, balance_ton, lang="ru"):
    asyncio.run_coroutine_threadsafe(
        _bot.send_message(
            user_id,
            fmt_deposit_credited(amount, currency, tx_hash, balance_usdt, balance_ton, lang),
            parse_mode="HTML",
        ),
        asyncio.get_event_loop(),
    )


def notify_admin(user_id, username, amount, currency, tx_hash,
                 unidentified=False, from_addr=None):
    from utils.messages import fmt_admin_deposit
    asyncio.run_coroutine_threadsafe(
        _bot.send_message(
            config.LOG_CHAT_ID,
            fmt_admin_deposit(
                user_id, username, amount, currency, tx_hash,
                unidentified=unidentified, from_addr=from_addr,
            ),
            parse_mode="HTML",
        ),
        asyncio.get_event_loop(),
    )


def notify_profit(user_id, profit_usdt, profit_ton,
                  balance_usdt, balance_ton, lang="ru"):
    asyncio.run_coroutine_threadsafe(
        _bot.send_message(
            user_id,
            fmt_profit_notification(profit_usdt, profit_ton, balance_usdt, balance_ton, lang),
            parse_mode="HTML",
        ),
        asyncio.get_event_loop(),
    )


# ─── Main ────────────────────────────────────────────────
async def main():
    global _bot

    db.init_db()

    _bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(user_handlers.router)
    dp.include_router(admin_handlers.router)

    set_notifiers(notify_user, notify_admin)
    set_profit_notifier(notify_profit)

    monitor.start()
    start_profit_scheduler()

    logger.info("╔══════════════════════════╗")
    logger.info("║  💎 Copy Pulse Bot START  ║")
    logger.info("╚══════════════════════════╝")
    logger.info("Polling started…")

    await dp.start_polling(_bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
