from config import config
from utils.i18n import t


def fmt_deposit_address(currency: str, user_id: int, lang: str = "ru") -> str:
    if currency == "TON":
        return t("deposit_address_ton", lang,
                 wallet=config.TON_WALLET,
                 minimum=f"{config.MIN_DEPOSIT_TON:.0f}",
                 user_id=user_id)
    else:
        return t("deposit_address_usdt", lang,
                 wallet=config.USDT_WALLET,
                 minimum=f"{config.MIN_DEPOSIT_USDT:.0f}",
                 user_id=user_id)


def fmt_balance(user: dict, lang: str = "ru") -> str:
    return t("balance", lang,
             usdt=user["balance_usdt"],
             ton=user["balance_ton"],
             dep_usdt=user["deposited_usdt"],
             dep_ton=user["deposited_ton"],
             staked=user.get("staked_usdt", 0),
             ref_earn=user.get("referral_earnings", 0))


def fmt_deposit_credited(amount: float, currency: str, tx_hash: str,
                         balance_usdt: float, balance_ton: float, lang: str = "ru") -> str:
    return t("deposit_credited", lang,
             amount=amount, currency=currency,
             tx_hash=tx_hash, usdt=balance_usdt, ton=balance_ton)


def fmt_profit_notification(profit_usdt: float, profit_ton: float,
                             balance_usdt: float, balance_ton: float, lang: str = "ru") -> str:
    lines = []
    if profit_usdt > 0:
        lines.append(f"💵 +<code>{profit_usdt:.4f}</code> USDT")
    if profit_ton > 0:
        lines.append(f"💎 +<code>{profit_ton:.6f}</code> TON")
    return t("profit_accrued", lang,
             profit_lines="\n".join(lines),
             usdt=balance_usdt, ton=balance_ton)


def fmt_admin_deposit(user_id, username, amount, currency, tx_hash,
                      unidentified=False, from_addr=None) -> str:
    if unidentified:
        return (
            f"⚠️ <b>НЕОПОЗНАННЫЙ ДЕПОЗИТ</b>\n\n"
            f"💵 Сумма: {amount:.2f} {currency}\n"
            f"📨 От: <code>{from_addr}</code>\n"
            f"🔑 Хэш: <code>{tx_hash}</code>\n\n"
            f"Требуется ручное зачисление!"
        )
    uname = f"@{username}" if username else f"ID:{user_id}"
    return (
        f"💰 <b>НОВЫЙ ДЕПОЗИТ (авто)</b>\n\n"
        f"👤 {uname} (ID: <code>{user_id}</code>)\n"
        f"💵 Сумма: <b>{amount:.2f} {currency}</b>\n"
        f"🔑 Хэш: <code>{tx_hash}</code>"
    )


def fmt_admin_withdraw(wid: int, user_id: int, username, amount: float,
                       currency: str, address: str) -> str:
    uname = f"@{username}" if username else f"ID:{user_id}"
    return (
        f"📤 <b>ЗАЯВКА НА ВЫВОД #{wid}</b>\n\n"
        f"👤 {uname} (ID: <code>{user_id}</code>)\n"
        f"💵 Сумма: <b>{amount:.2f} {currency}</b>\n"
        f"📬 Адрес: <code>{address}</code>"
    )
