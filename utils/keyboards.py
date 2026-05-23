from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import STAKING_PLANS, TRADERS
from utils.i18n import t


# ─── Main menu ───────────────────────────────────────────
def main_menu(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💼 Баланс" if lang == "ru" else "💼 Balance", callback_data="balance"),
            InlineKeyboardButton(text="📥 Пополнить" if lang == "ru" else "📥 Deposit", callback_data="deposit"),
        ],
        [
            InlineKeyboardButton(text="📤 Вывести" if lang == "ru" else "📤 Withdraw", callback_data="withdraw"),
            InlineKeyboardButton(text="📊 Статистика" if lang == "ru" else "📊 Statistics", callback_data="stats"),
        ],
        [
            InlineKeyboardButton(text="📡 Копитрейдинг" if lang == "ru" else "📡 Copy Trading", callback_data="copy_menu"),
            InlineKeyboardButton(text="🏦 Стейкинг" if lang == "ru" else "🏦 Staking", callback_data="staking_menu"),
        ],
        [
            InlineKeyboardButton(text="🤝 Рефералы" if lang == "ru" else "🤝 Referrals", callback_data="referral"),
            InlineKeyboardButton(text="📋 История" if lang == "ru" else "📋 History", callback_data="history_0"),
        ],
        [
            InlineKeyboardButton(text="❓ Помощь" if lang == "ru" else "❓ Help", callback_data="help"),
            InlineKeyboardButton(text="🌐 Язык" if lang == "ru" else "🌐 Language", callback_data="language"),
        ],
        [
            InlineKeyboardButton(text="🆘 Поддержка" if lang == "ru" else "🆘 Support", callback_data="support"),
        ],
    ])


# ─── Back to menu ────────────────────────────────────────
def back_to_menu_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("main_menu_btn", lang), callback_data="main_menu")]
    ])


# ─── Deposit ─────────────────────────────────────────────
def deposit_currency_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 TON", callback_data="dep_ton"),
            InlineKeyboardButton(text="💵 USDT (TRC-20)", callback_data="dep_usdt"),
        ],
        [InlineKeyboardButton(text=t("back", lang), callback_data="main_menu")],
    ])


def deposit_confirm_kb(currency: str, lang: str = "ru") -> InlineKeyboardMarkup:
    btn_text = "✅ Я отправил" if lang == "ru" else "✅ I sent it"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, callback_data=f"sent_{currency.lower()}")],
        [InlineKeyboardButton(text=t("back", lang), callback_data="deposit")],
    ])


# ─── Withdraw ────────────────────────────────────────────
def withdraw_currency_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 TON", callback_data="with_ton"),
            InlineKeyboardButton(text="💵 USDT (TRC-20)", callback_data="with_usdt"),
        ],
        [InlineKeyboardButton(text=t("back", lang), callback_data="main_menu")],
    ])


# ─── Admin: withdraw approval ────────────────────────────
def admin_withdraw_kb(wid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Одобрить", callback_data=f"aw_approve_{wid}"),
            InlineKeyboardButton(text="❌ Отклонить", callback_data=f"aw_reject_{wid}"),
        ]
    ])


# ─── Language ────────────────────────────────────────────
def language_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
        ],
        [InlineKeyboardButton(text="⬅️ Назад / Back", callback_data="main_menu")],
    ])


# ─── Copy trading ─────────────────────────────────────────
def copy_menu_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    btn1 = "📋 Список трейдеров" if lang == "ru" else "📋 Traders List"
    btn2 = "📡 Мои позиции" if lang == "ru" else "📡 My Positions"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn1, callback_data="copy_traders")],
        [InlineKeyboardButton(text=btn2, callback_data="copy_my")],
        [InlineKeyboardButton(text=t("back", lang), callback_data="main_menu")],
    ])


def traders_list_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for tr in TRADERS:
        winrate = tr["win"] / tr["total"] * 100
        label = f"{tr['flag']} {tr['name']} | {winrate:.0f}% | +{tr['monthly']:.1f}%/мес"
        if lang == "en":
            label = f"{tr['flag']} {tr['name']} | {winrate:.0f}% | +{tr['monthly']:.1f}%/mo"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"copy_trader_{tr['id']}")])
    buttons.append([InlineKeyboardButton(text=t("back", lang), callback_data="copy_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def copy_positions_kb(positions: list, lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for pos in positions:
        label = f"❌ {pos['trader_id']} | {pos['amount']:.2f} USDT"
        close_txt = "Закрыть" if lang == "ru" else "Close"
        buttons.append([InlineKeyboardButton(
            text=f"{close_txt}: {label}",
            callback_data=f"copy_close_{pos['id']}"
        )])
    buttons.append([InlineKeyboardButton(text=t("back", lang), callback_data="copy_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ─── Staking ─────────────────────────────────────────────
def staking_menu_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    btn1 = "🆕 Открыть позицию" if lang == "ru" else "🆕 Open Position"
    btn2 = "📂 Мои позиции" if lang == "ru" else "📂 My Positions"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn1, callback_data="staking_plans")],
        [InlineKeyboardButton(text=btn2, callback_data="staking_my")],
        [InlineKeyboardButton(text=t("back", lang), callback_data="main_menu")],
    ])


def staking_plans_kb(lang: str = "ru") -> InlineKeyboardMarkup:
    buttons = []
    for plan in STAKING_PLANS:
        name = plan["name_ru"] if lang == "ru" else plan["name_en"]
        lock = f"{plan['lock_days']}д" if lang == "ru" else f"{plan['lock_days']}d"
        if plan["lock_days"] == 0:
            lock = "Нет" if lang == "ru" else "None"
        label = f"{plan['emoji']} {name} | {plan['daily_pct']}%/д | мин {plan['min_usdt']}$"
        if lang == "en":
            label = f"{plan['emoji']} {name} | {plan['daily_pct']}%/d | min ${plan['min_usdt']}"
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"stake_plan_{plan['id']}")])
    buttons.append([InlineKeyboardButton(text=t("back", lang), callback_data="staking_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def staking_positions_kb(positions: list, lang: str = "ru") -> InlineKeyboardMarkup:
    import time
    buttons = []
    for pos in positions:
        can_close = pos["lock_days"] == 0 or (pos["unlock_at"] > 0 and time.time() >= pos["unlock_at"])
        if can_close:
            close_txt = f"🔓 Закрыть #{pos['id']} | {pos['amount']:.2f} USDT"
            if lang == "en":
                close_txt = f"🔓 Close #{pos['id']} | {pos['amount']:.2f} USDT"
            buttons.append([InlineKeyboardButton(text=close_txt, callback_data=f"stake_close_{pos['id']}")])
        else:
            locked_txt = f"🔒 #{pos['id']} | {pos['amount']:.2f} USDT (заблокирован)"
            if lang == "en":
                locked_txt = f"🔒 #{pos['id']} | {pos['amount']:.2f} USDT (locked)"
            buttons.append([InlineKeyboardButton(text=locked_txt, callback_data="staking_locked_notice")])
    buttons.append([InlineKeyboardButton(text=t("back", lang), callback_data="staking_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ─── History ─────────────────────────────────────────────
def history_kb(page: int, total_pages: int, lang: str = "ru") -> InlineKeyboardMarkup:
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️", callback_data=f"history_{page - 1}"))
    if page < total_pages - 1:
        nav.append(InlineKeyboardButton(text="▶️", callback_data=f"history_{page + 1}"))
    buttons = []
    if nav:
        buttons.append(nav)
    buttons.append([InlineKeyboardButton(text=t("main_menu_btn", lang), callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
