import logging
import time
import math
from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import db.database as db
from config import config, STAKING_PLANS, TRADERS
from utils.i18n import t
from utils.keyboards import (
    main_menu, deposit_currency_kb, deposit_confirm_kb,
    withdraw_currency_kb, back_to_menu_kb, language_kb,
    copy_menu_kb, traders_list_kb, copy_positions_kb,
    staking_menu_kb, staking_plans_kb, staking_positions_kb,
    history_kb, admin_withdraw_kb,
)
from utils.messages import fmt_balance, fmt_deposit_address, fmt_admin_withdraw

logger = logging.getLogger(__name__)
router = Router()


# ─── FSM States ────────────────────────────────────────────
class WithdrawForm(StatesGroup):
    choosing_currency = State()
    entering_amount   = State()
    entering_address  = State()


class DepositForm(StatesGroup):
    choosing_currency = State()
    entering_amount   = State()


class StakingForm(StatesGroup):
    entering_amount = State()


class CopyForm(StatesGroup):
    entering_amount = State()


# ─── Helpers ───────────────────────────────────────────────
def _lang(user_id: int) -> str:
    user = db.get_user(user_id)
    return user.get("language", "ru") if user else "ru"


def _trader_by_id(trader_id: str) -> dict | None:
    return next((tr for tr in TRADERS if tr["id"] == trader_id), None)


def _plan_by_id(plan_id: int) -> dict | None:
    return next((p for p in STAKING_PLANS if p["id"] == plan_id), None)


def _fmt_date(ts: int) -> str:
    if not ts:
        return "—"
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%d.%m.%Y")


def _risk_label(risk: str, lang: str) -> str:
    labels = {
        "ru": {"low": "🟢 Низкий", "medium": "🟡 Средний", "high": "🔴 Высокий"},
        "en": {"low": "🟢 Low", "medium": "🟡 Medium", "high": "🔴 High"},
    }
    return labels.get(lang, labels["ru"]).get(risk, risk)


# ─── /start ────────────────────────────────────────────────
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    args = message.text.split(maxsplit=1)
    ref_code = args[1].strip() if len(args) > 1 else None
    db.upsert_user(message.from_user.id, message.from_user.username, ref_code)
    lang = _lang(message.from_user.id)
    name = message.from_user.first_name or message.from_user.username or "User"
    await message.answer(
        t("welcome", lang,
          name=name,
          pct=config.DAILY_PROFIT_PCT,
          min_ton=int(config.MIN_DEPOSIT_TON),
          min_usdt=int(config.MIN_DEPOSIT_USDT)),
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )


# ─── Main menu ─────────────────────────────────────────────
@router.callback_query(F.data == "main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("main_menu_title", lang),
        reply_markup=main_menu(lang),
        parse_mode="HTML",
    )


# ─── Balance ───────────────────────────────────────────────
@router.callback_query(F.data == "balance")
async def cb_balance(call: CallbackQuery):
    db.upsert_user(call.from_user.id, call.from_user.username)
    user = db.get_user(call.from_user.id)
    lang = user.get("language", "ru")
    await call.message.edit_text(
        fmt_balance(user, lang),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Stats ─────────────────────────────────────────────────
@router.callback_query(F.data == "stats")
async def cb_stats(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    if not user:
        db.upsert_user(call.from_user.id, call.from_user.username)
        user = db.get_user(call.from_user.id)
    lang = user.get("language", "ru")
    pct = config.DAILY_PROFIT_PCT
    daily_usdt = user["balance_usdt"] * pct / 100
    daily_ton  = user["balance_ton"] * pct / 100
    await call.message.edit_text(
        t("stats", lang,
          usdt=user["balance_usdt"], ton=user["balance_ton"],
          pct=pct, daily_usdt=daily_usdt, daily_ton=daily_ton,
          dep_usdt=user["deposited_usdt"], dep_ton=user["deposited_ton"],
          staked=user.get("staked_usdt", 0),
          ref_earn=user.get("referral_earnings", 0)),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Deposit ───────────────────────────────────────────────
@router.callback_query(F.data == "deposit")
async def cb_deposit(call: CallbackQuery, state: FSMContext):
    await state.set_state(DepositForm.choosing_currency)
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("deposit_choose", lang),
        reply_markup=deposit_currency_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.in_({"dep_ton", "dep_usdt"}))
async def cb_deposit_currency(call: CallbackQuery, state: FSMContext):
    currency = "TON" if call.data == "dep_ton" else "USDT"
    lang = _lang(call.from_user.id)
    await state.update_data(currency=currency)
    await state.set_state(DepositForm.entering_amount)
    text = fmt_deposit_address(currency, call.from_user.id, lang)
    await call.message.edit_text(
        text,
        reply_markup=deposit_confirm_kb(currency, lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.in_({"sent_ton", "sent_usdt"}))
async def cb_sent(call: CallbackQuery, state: FSMContext):
    currency = "TON" if call.data == "sent_ton" else "USDT"
    lang = _lang(call.from_user.id)
    await state.update_data(currency=currency)
    await state.set_state(DepositForm.entering_amount)
    await call.message.edit_text(
        t("deposit_enter_amount", lang, currency=currency),
        parse_mode="HTML",
    )


@router.message(DepositForm.entering_amount)
async def process_deposit_amount(message: Message, state: FSMContext):
    lang = _lang(message.from_user.id)
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer(t("invalid_number", lang), parse_mode="HTML")
        return
    data = await state.get_data()
    currency = data.get("currency", "USDT")
    minimum = config.MIN_DEPOSIT_TON if currency == "TON" else config.MIN_DEPOSIT_USDT
    if amount < minimum:
        await message.answer(t("deposit_too_small", lang, minimum=minimum, currency=currency), parse_mode="HTML")
        return
    db.add_pending_deposit(message.from_user.id, amount, currency)
    await state.clear()
    await message.answer(
        t("deposit_pending", lang, amount=amount, currency=currency, user_id=message.from_user.id),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Withdraw ──────────────────────────────────────────────
@router.callback_query(F.data == "withdraw")
async def cb_withdraw(call: CallbackQuery, state: FSMContext):
    await state.set_state(WithdrawForm.choosing_currency)
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("withdraw_choose", lang),
        reply_markup=withdraw_currency_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.in_({"with_ton", "with_usdt"}))
async def cb_withdraw_currency(call: CallbackQuery, state: FSMContext):
    currency = "TON" if call.data == "with_ton" else "USDT"
    lang = _lang(call.from_user.id)
    await state.update_data(currency=currency)
    await state.set_state(WithdrawForm.entering_amount)
    user = db.get_user(call.from_user.id)
    balance = user["balance_ton"] if currency == "TON" else user["balance_usdt"]
    minimum = config.MIN_WITHDRAW_TON if currency == "TON" else config.MIN_WITHDRAW_USDT
    await call.message.edit_text(
        t("withdraw_enter_amount", lang, balance=balance, currency=currency, minimum=minimum),
        parse_mode="HTML",
    )


@router.message(WithdrawForm.entering_amount)
async def process_withdraw_amount(message: Message, state: FSMContext):
    lang = _lang(message.from_user.id)
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer(t("withdraw_bad_amount", lang), parse_mode="HTML")
        return
    data = await state.get_data()
    currency = data.get("currency", "USDT")
    user = db.get_user(message.from_user.id)
    balance = user["balance_ton"] if currency == "TON" else user["balance_usdt"]
    minimum = config.MIN_WITHDRAW_TON if currency == "TON" else config.MIN_WITHDRAW_USDT
    if amount < minimum:
        await message.answer(t("withdraw_too_small", lang, minimum=minimum, currency=currency), parse_mode="HTML")
        return
    if amount > balance:
        await message.answer(t("withdraw_insufficient", lang, balance=balance, currency=currency), parse_mode="HTML")
        return
    await state.update_data(amount=amount)
    await state.set_state(WithdrawForm.entering_address)
    hint_key = "withdraw_enter_address_ton" if currency == "TON" else "withdraw_enter_address_usdt"
    await message.answer(t(hint_key, lang), parse_mode="HTML")


@router.message(WithdrawForm.entering_address)
async def process_withdraw_address(message: Message, state: FSMContext, bot):
    address = message.text.strip()
    data = await state.get_data()
    currency = data["currency"]
    amount = data["amount"]
    user_id = message.from_user.id
    lang = _lang(user_id)

    if currency == "TON" and not address.startswith(("UQ", "EQ")):
        await message.answer(t("withdraw_bad_ton_addr", lang), parse_mode="HTML")
        return
    if currency == "USDT" and not address.startswith("T"):
        await message.answer(t("withdraw_bad_usdt_addr", lang), parse_mode="HTML")
        return

    db.debit_balance(user_id, amount, currency)
    wid = db.create_withdraw(user_id, amount, currency, address)
    await state.clear()
    await message.answer(
        t("withdraw_created", lang, amount=amount, currency=currency, wid=wid),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )

    user = db.get_user(user_id)
    await bot.send_message(
        config.LOG_CHAT_ID,
        fmt_admin_withdraw(wid, user_id, user["username"] if user else None, amount, currency, address),
        reply_markup=admin_withdraw_kb(wid),
        parse_mode="HTML",
    )


# ─── History ───────────────────────────────────────────────
@router.callback_query(F.data.startswith("history_"))
async def cb_history(call: CallbackQuery):
    page = int(call.data.split("_")[1])
    lang = _lang(call.from_user.id)
    page_size = config.HISTORY_PAGE_SIZE
    total = db.count_user_operations(call.from_user.id)

    if total == 0:
        await call.message.edit_text(
            t("history_empty", lang),
            reply_markup=back_to_menu_kb(lang),
            parse_mode="HTML",
        )
        return

    total_pages = math.ceil(total / page_size)
    page = max(0, min(page, total_pages - 1))
    ops = db.get_user_operations(call.from_user.id, limit=page_size, offset=page * page_size)

    type_icons = {
        "deposit":      "📥",
        "withdraw":     "📤",
        "profit":       "💹",
        "staking_open": "🔒",
        "staking_close":"🔓",
        "copy_open":    "📡",
        "copy_close":   "📡",
        "referral_bonus":"🤝",
    }

    lines = [t("history_title", lang), ""]
    for op in ops:
        icon = type_icons.get(op["op_type"], "🔹")
        date = datetime.fromtimestamp(op["created_at"], tz=timezone.utc).strftime("%d.%m %H:%M")
        sign = "+" if op["op_type"] in ("deposit", "profit", "staking_close", "copy_close", "referral_bonus") else "-"
        lines.append(
            f"{icon} <code>{date}</code>  {sign}<b>{op['amount']:.2f}</b> {op['currency']}\n"
            f"   <i>{op['description']}</i>"
        )

    lines.append(f"\n{t('history_page', lang, page=page+1, total=total_pages)}")
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=history_kb(page, total_pages, lang),
        parse_mode="HTML",
    )


# ─── Support ───────────────────────────────────────────────
@router.callback_query(F.data == "support")
async def cb_support(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("support", lang, support=config.SUPPORT_USER),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Help ──────────────────────────────────────────────────
@router.callback_query(F.data == "help")
async def cb_help(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("help", lang,
          min_ton=int(config.MIN_DEPOSIT_TON),
          min_usdt=int(config.MIN_DEPOSIT_USDT),
          min_w_ton=int(config.MIN_WITHDRAW_TON),
          min_w_usdt=int(config.MIN_WITHDRAW_USDT),
          ref_pct=int(config.REFERRAL_BONUS_PCT),
          support=config.SUPPORT_USER),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Language ──────────────────────────────────────────────
@router.callback_query(F.data == "language")
async def cb_language(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("language_choose", lang),
        reply_markup=language_kb(),
        parse_mode="HTML",
    )


@router.callback_query(F.data.in_({"lang_ru", "lang_en"}))
async def cb_set_language(call: CallbackQuery):
    new_lang = call.data.split("_")[1]
    db.set_language(call.from_user.id, new_lang)
    key = "language_changed_ru" if new_lang == "ru" else "language_changed_en"
    await call.message.edit_text(
        t(key, new_lang),
        reply_markup=main_menu(new_lang),
        parse_mode="HTML",
    )


# ─── Referral ──────────────────────────────────────────────
@router.callback_query(F.data == "referral")
async def cb_referral(call: CallbackQuery):
    user = db.get_user(call.from_user.id)
    if not user:
        db.upsert_user(call.from_user.id, call.from_user.username)
        user = db.get_user(call.from_user.id)
    lang = user.get("language", "ru")
    ref_code = user["referral_code"]
    bot_info_link = f"https://t.me/CopyPulseBot?start={ref_code}"
    refs = db.get_user_referrals(call.from_user.id)
    await call.message.edit_text(
        t("referral_title", lang,
          link=bot_info_link,
          pct=int(config.REFERRAL_BONUS_PCT),
          count=len(refs),
          earned=user.get("referral_earnings", 0)),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Copy Trading ──────────────────────────────────────────
@router.callback_query(F.data == "copy_menu")
async def cb_copy_menu(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("copy_title", lang),
        reply_markup=copy_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "copy_traders")
async def cb_copy_traders(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("copy_traders_list", lang),
        reply_markup=traders_list_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("copy_trader_"))
async def cb_copy_trader_select(call: CallbackQuery, state: FSMContext):
    trader_id = call.data[len("copy_trader_"):]
    trader = _trader_by_id(trader_id)
    if not trader:
        await call.answer("Трейдер не найден", show_alert=True)
        return
    lang = _lang(call.from_user.id)
    winrate = trader["win"] / trader["total"] * 100
    strategy = trader["strategy_ru"] if lang == "ru" else trader["strategy_en"]
    await state.update_data(trader_id=trader_id)
    await state.set_state(CopyForm.entering_amount)
    await call.message.edit_text(
        t("copy_trader_card", lang,
          name=trader["name"],
          flag=trader["flag"],
          win=trader["win"],
          total=trader["total"],
          winrate=winrate,
          monthly=trader["monthly"],
          followers=trader["followers"],
          risk=_risk_label(trader["risk"], lang),
          strategy=strategy),
        parse_mode="HTML",
    )


@router.message(CopyForm.entering_amount)
async def process_copy_amount(message: Message, state: FSMContext):
    lang = _lang(message.from_user.id)
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer(t("invalid_number", lang), parse_mode="HTML")
        return
    if amount < 10:
        await message.answer("❌ Минимум: 10 USDT" if lang == "ru" else "❌ Minimum: 10 USDT")
        return
    user = db.get_user(message.from_user.id)
    if user["balance_usdt"] < amount:
        await message.answer(t("copy_insufficient", lang), parse_mode="HTML")
        return
    data = await state.get_data()
    trader_id = data.get("trader_id")
    trader = _trader_by_id(trader_id)
    db.create_copy_position(message.from_user.id, trader_id, amount)
    await state.clear()
    await message.answer(
        t("copy_opened", lang, trader=trader["name"] if trader else trader_id, amount=amount),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "copy_my")
async def cb_copy_my(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    positions = db.get_user_copy_positions(call.from_user.id)
    if not positions:
        await call.message.edit_text(
            f"{t('copy_my_positions', lang)}\n\n{t('copy_no_positions', lang)}",
            reply_markup=back_to_menu_kb(lang),
            parse_mode="HTML",
        )
        return
    lines = [t("copy_my_positions", lang), ""]
    for pos in positions:
        trader = _trader_by_id(pos["trader_id"])
        name = trader["name"] if trader else pos["trader_id"]
        lines.append(
            t("copy_position_item", lang,
              trader=name,
              amount=pos["amount"],
              date=_fmt_date(pos["started_at"]),
              earned=pos.get("total_earned", 0))
        )
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=copy_positions_kb(positions, lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("copy_close_"))
async def cb_copy_close(call: CallbackQuery):
    pos_id = int(call.data.split("_")[2])
    lang = _lang(call.from_user.id)
    positions = db.get_user_copy_positions(call.from_user.id)
    pos = next((p for p in positions if p["id"] == pos_id), None)
    if not pos:
        await call.answer("Позиция не найдена", show_alert=True)
        return
    elapsed_days = (time.time() - pos["started_at"]) / 86400
    trader = _trader_by_id(pos["trader_id"])
    monthly_pct = trader["monthly"] if trader else 5.0
    daily_pct = monthly_pct / 30
    earned = round(pos["amount"] * daily_pct / 100 * elapsed_days, 4)
    db.close_copy_position(pos_id, call.from_user.id, pos["amount"], earned)
    await call.message.edit_text(
        t("copy_closed", lang),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


# ─── Staking ───────────────────────────────────────────────
@router.callback_query(F.data == "staking_menu")
async def cb_staking_menu(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("staking_title", lang),
        reply_markup=staking_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "staking_plans")
async def cb_staking_plans(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.message.edit_text(
        t("staking_title", lang),
        reply_markup=staking_plans_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("stake_plan_"))
async def cb_stake_plan(call: CallbackQuery, state: FSMContext):
    plan_id = int(call.data.split("_")[2])
    plan = _plan_by_id(plan_id)
    if not plan:
        await call.answer("План не найден", show_alert=True)
        return
    lang = _lang(call.from_user.id)
    user = db.get_user(call.from_user.id)
    name = plan["name_ru"] if lang == "ru" else plan["name_en"]
    desc = plan["desc_ru"] if lang == "ru" else plan["desc_en"]
    lock_str = desc
    await state.update_data(plan_id=plan_id)
    await state.set_state(StakingForm.entering_amount)
    await call.message.edit_text(
        t("staking_plan_info", lang,
          emoji=plan["emoji"],
          name=name,
          pct=plan["daily_pct"],
          min_usdt=plan["min_usdt"],
          lock=lock_str,
          balance=user["balance_usdt"]),
        parse_mode="HTML",
    )


@router.message(StakingForm.entering_amount)
async def process_staking_amount(message: Message, state: FSMContext):
    lang = _lang(message.from_user.id)
    try:
        amount = float(message.text.strip().replace(",", "."))
    except ValueError:
        await message.answer(t("invalid_number", lang), parse_mode="HTML")
        return
    data = await state.get_data()
    plan_id = data.get("plan_id")
    plan = _plan_by_id(plan_id)
    if not plan:
        await state.clear()
        return
    if amount < plan["min_usdt"]:
        await message.answer(t("staking_insufficient", lang, min_usdt=plan["min_usdt"]), parse_mode="HTML")
        return
    user = db.get_user(message.from_user.id)
    if user["balance_usdt"] < amount:
        await message.answer(t("staking_insufficient", lang, min_usdt=plan["min_usdt"]), parse_mode="HTML")
        return
    pos_id = db.create_staking(
        message.from_user.id, plan_id, amount, plan["daily_pct"], plan["lock_days"]
    )
    await state.clear()
    name = plan["name_ru"] if lang == "ru" else plan["name_en"]
    desc = plan["desc_ru"] if lang == "ru" else plan["desc_en"]
    unlock_date = "Любое время" if plan["lock_days"] == 0 else _fmt_date(int(time.time()) + plan["lock_days"] * 86400)
    if lang == "en":
        unlock_date = "Anytime" if plan["lock_days"] == 0 else _fmt_date(int(time.time()) + plan["lock_days"] * 86400)
    await message.answer(
        t("staking_opened", lang,
          emoji=plan["emoji"],
          name=name,
          amount=amount,
          pct=plan["daily_pct"],
          unlock=unlock_date),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "staking_my")
async def cb_staking_my(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    positions = db.get_user_staking(call.from_user.id)
    if not positions:
        await call.message.edit_text(
            f"{t('staking_my_title', lang)}\n\n{t('staking_no_positions', lang)}",
            reply_markup=back_to_menu_kb(lang),
            parse_mode="HTML",
        )
        return
    lines = [t("staking_my_title", lang), ""]
    for pos in positions:
        plan = _plan_by_id(pos["plan_id"])
        emoji = plan["emoji"] if plan else "🏦"
        name = (plan["name_ru"] if lang == "ru" else plan["name_en"]) if plan else f"Plan {pos['plan_id']}"
        unlock = "∞" if pos["lock_days"] == 0 else _fmt_date(pos["unlock_at"])
        elapsed = (time.time() - pos["started_at"]) / 86400
        earned = round(pos["amount"] * pos["daily_pct"] / 100 * elapsed, 4)
        lines.append(
            t("staking_position_item", lang,
              emoji=emoji, name=name,
              amount=pos["amount"], pct=pos["daily_pct"],
              unlock=unlock, earned=earned)
        )
    await call.message.edit_text(
        "\n".join(lines),
        reply_markup=staking_positions_kb(positions, lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "staking_locked_notice")
async def cb_staking_locked(call: CallbackQuery):
    lang = _lang(call.from_user.id)
    await call.answer(
        "🔒 Позиция заблокирована" if lang == "ru" else "🔒 Position is locked",
        show_alert=True
    )


@router.callback_query(F.data.startswith("stake_close_"))
async def cb_stake_close(call: CallbackQuery):
    pos_id = int(call.data.split("_")[2])
    lang = _lang(call.from_user.id)
    positions = db.get_user_staking(call.from_user.id)
    pos = next((p for p in positions if p["id"] == pos_id), None)
    if not pos:
        await call.answer("Позиция не найдена", show_alert=True)
        return
    elapsed = (time.time() - pos["started_at"]) / 86400
    earned = round(pos["amount"] * pos["daily_pct"] / 100 * elapsed, 4)
    db.close_staking(pos_id, call.from_user.id, pos["amount"], earned)
    await call.message.edit_text(
        t("staking_closed", lang),
        reply_markup=back_to_menu_kb(lang),
        parse_mode="HTML",
    )
