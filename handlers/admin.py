import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import db.database as db
from config import config
from utils.keyboards import back_to_menu_kb, admin_withdraw_kb

logger = logging.getLogger(__name__)
router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == config.LOG_CHAT_ID


# ─── Withdraw: approve / reject ────────────────────────────
@router.callback_query(F.data.startswith("aw_approve_"))
async def cb_approve_withdraw(call: CallbackQuery, bot):
    wid = int(call.data.split("_")[-1])
    wr = db.get_withdraw_by_id(wid)
    db.update_withdraw_status(wid, "approved")
    await call.message.edit_text(
        call.message.text + "\n\n✅ <b>ОДОБРЕНО</b>",
        parse_mode="HTML",
    )
    if wr:
        try:
            user = db.get_user(wr["user_id"])
            lang = user.get("language", "ru") if user else "ru"
            text = (
                f"✅ <b>Ваша заявка на вывод #{wid} одобрена!</b>\n\n"
                f"💰 Сумма: <code>{wr['amount']:.2f} {wr['currency']}</code>\n"
                f"⏳ Перевод будет выполнен в ближайшее время."
            ) if lang == "ru" else (
                f"✅ <b>Your withdrawal request #{wid} approved!</b>\n\n"
                f"💰 Amount: <code>{wr['amount']:.2f} {wr['currency']}</code>\n"
                f"⏳ Transfer will be processed shortly."
            )
            await bot.send_message(wr["user_id"], text, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Cannot notify user about withdrawal approval: {e}")
    await call.answer("✅ Заявка одобрена")
    logger.info(f"[ADMIN] Withdraw #{wid} approved by {call.from_user.id}")


@router.callback_query(F.data.startswith("aw_reject_"))
async def cb_reject_withdraw(call: CallbackQuery, bot):
    wid = int(call.data.split("_")[-1])
    wr = db.get_withdraw_by_id(wid)
    db.update_withdraw_status(wid, "rejected")
    # Refund the balance
    if wr:
        db.credit_deposit(wr["user_id"], wr["amount"], wr["currency"])
        try:
            user = db.get_user(wr["user_id"])
            lang = user.get("language", "ru") if user else "ru"
            text = (
                f"❌ <b>Ваша заявка на вывод #{wid} отклонена.</b>\n\n"
                f"💰 Сумма <code>{wr['amount']:.2f} {wr['currency']}</code> возвращена на баланс."
            ) if lang == "ru" else (
                f"❌ <b>Your withdrawal request #{wid} rejected.</b>\n\n"
                f"💰 Amount <code>{wr['amount']:.2f} {wr['currency']}</code> refunded to balance."
            )
            await bot.send_message(wr["user_id"], text, parse_mode="HTML")
        except Exception as e:
            logger.warning(f"Cannot notify user about withdrawal rejection: {e}")
    await call.message.edit_text(
        call.message.text + "\n\n❌ <b>ОТКЛОНЕНО</b>",
        parse_mode="HTML",
    )
    await call.answer("❌ Заявка отклонена")


# ─── /admin_stats ───────────────────────────────────────────
@router.message(Command("admin_stats"))
async def cmd_admin_stats(message: Message):
    if not is_admin(message.from_user.id):
        return
    users = db.get_all_users()
    total_usdt  = sum(u["deposited_usdt"] for u in users)
    total_ton   = sum(u["deposited_ton"] for u in users)
    bal_usdt    = sum(u["balance_usdt"] for u in users)
    bal_ton     = sum(u["balance_ton"] for u in users)
    staked_usdt = sum(u.get("staked_usdt", 0) for u in users)
    ref_earn    = sum(u.get("referral_earnings", 0) for u in users)

    await message.answer(
        f"╔═══════════════════════╗\n"
        f"║   📊 <b>ADMIN СТАТИСТИКА</b>  ║\n"
        f"╚═══════════════════════╝\n\n"
        f"👥 <b>Пользователей:</b> {len(users)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Внесено всего:</b>\n"
        f"  • USDT: <code>{total_usdt:.2f}</code>\n"
        f"  • TON:  <code>{total_ton:.4f}</code>\n\n"
        f"📈 <b>Текущие балансы:</b>\n"
        f"  • USDT: <code>{bal_usdt:.2f}</code>\n"
        f"  • TON:  <code>{bal_ton:.4f}</code>\n\n"
        f"🔒 <b>В стейкинге:</b> <code>{staked_usdt:.2f}</code> USDT\n"
        f"🤝 <b>Реф. доход всего:</b> <code>{ref_earn:.2f}</code> USDT",
        parse_mode="HTML",
    )


# ─── /admin_credit ────────────────────────────────────────
@router.message(Command("admin_credit"))
async def cmd_admin_credit(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 4:
        await message.answer(
            "Использование: <code>/admin_credit &lt;user_id&gt; &lt;amount&gt; &lt;TON|USDT&gt;</code>",
            parse_mode="HTML"
        )
        return
    try:
        uid      = int(parts[1])
        amount   = float(parts[2])
        currency = parts[3].upper()
        assert currency in ("TON", "USDT")
    except Exception:
        await message.answer("❌ Неверные параметры.")
        return
    user = db.get_user(uid)
    if not user:
        await message.answer("❌ Пользователь не найден.")
        return
    db.credit_deposit(uid, amount, currency)
    await message.answer(
        f"✅ Зачислено <b>{amount:.2f} {currency}</b> пользователю <code>{uid}</code>",
        parse_mode="HTML",
    )


# ─── /admin_pending ─────────────────────────────────────────
@router.message(Command("admin_pending"))
async def cmd_admin_pending(message: Message):
    if not is_admin(message.from_user.id):
        return
    withdrawals = db.get_pending_withdrawals()
    if not withdrawals:
        await message.answer("✅ Нет ожидающих заявок на вывод.")
        return
    lines = [f"📤 <b>Заявки на вывод ({len(withdrawals)})</b>\n"]
    for w in withdrawals:
        lines.append(
            f"<b>#{w['id']}</b> | <code>{w['amount']:.2f} {w['currency']}</code>\n"
            f"→ <code>{w['address']}</code>\n"
            f"👤 User: <code>{w['user_id']}</code>"
        )
    await message.answer("\n\n".join(lines), parse_mode="HTML")


# ─── /broadcast ─────────────────────────────────────────────
class BroadcastState(StatesGroup):
    waiting_text = State()


@router.message(Command("broadcast"))
async def cmd_broadcast_start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    await state.set_state(BroadcastState.waiting_text)
    await message.answer("✏️ Введите текст рассылки (поддерживается HTML):")


@router.message(BroadcastState.waiting_text)
async def cmd_broadcast_send(message: Message, state: FSMContext, bot):
    if not is_admin(message.from_user.id):
        return
    await state.clear()
    users = db.get_all_users()
    ok = fail = 0
    for u in users:
        try:
            await bot.send_message(u["tg_id"], message.text, parse_mode="HTML")
            ok += 1
        except Exception:
            fail += 1
    await message.answer(
        f"📣 <b>Рассылка завершена</b>\n✅ Доставлено: {ok} / ❌ Ошибок: {fail}",
        parse_mode="HTML"
    )
