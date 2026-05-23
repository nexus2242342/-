"""
Internationalization module — RU / EN translations.
"""

TEXTS = {

    # ──────────────── START ────────────────
    "welcome": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   💎 <b>COPY PULSE</b>       ║\n"
            "╚═══════════════════════╝\n\n"
            "👋 Добро пожаловать, <b>{name}</b>!\n\n"
            "🤖 Автоматическая платформа копи-трейдинга\n"
            "📈 Доходность: <b>{pct}% в день</b>\n"
            "💰 Мин. депозит: <b>{min_ton} TON / {min_usdt} USDT</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Выберите действие ниже 👇"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   💎 <b>COPY PULSE</b>       ║\n"
            "╚═══════════════════════╝\n\n"
            "👋 Welcome, <b>{name}</b>!\n\n"
            "🤖 Automated copy-trading platform\n"
            "📈 Daily yield: <b>{pct}% per day</b>\n"
            "💰 Min. deposit: <b>{min_ton} TON / {min_usdt} USDT</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Choose an action below 👇"
        ),
    },

    "main_menu_title": {
        "ru": "🏠 <b>Главное меню</b>",
        "en": "🏠 <b>Main Menu</b>",
    },

    # ──────────────── BALANCE ────────────────
    "balance": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   💼 <b>ВАШ БАЛАНС</b>      ║\n"
            "╚═══════════════════════╝\n\n"
            "💵 <b>USDT:</b>  <code>{usdt:.2f}</code> USDT\n"
            "💎 <b>TON:</b>   <code>{ton:.4f}</code> TON\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>Внесено всего:</b>\n"
            "  • USDT: <code>{dep_usdt:.2f}</code>\n"
            "  • TON:  <code>{dep_ton:.4f}</code>\n\n"
            "🔒 <b>В стейкинге:</b> <code>{staked:.2f}</code> USDT\n"
            "🤝 <b>Реф. доход:</b>  <code>{ref_earn:.2f}</code> USDT"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   💼 <b>YOUR BALANCE</b>     ║\n"
            "╚═══════════════════════╝\n\n"
            "💵 <b>USDT:</b>  <code>{usdt:.2f}</code> USDT\n"
            "💎 <b>TON:</b>   <code>{ton:.4f}</code> TON\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>Total deposited:</b>\n"
            "  • USDT: <code>{dep_usdt:.2f}</code>\n"
            "  • TON:  <code>{dep_ton:.4f}</code>\n\n"
            "🔒 <b>Staked:</b>        <code>{staked:.2f}</code> USDT\n"
            "🤝 <b>Ref. earnings:</b> <code>{ref_earn:.2f}</code> USDT"
        ),
    },

    # ──────────────── DEPOSIT ────────────────
    "deposit_choose": {
        "ru": "📥 <b>Пополнение</b>\n\nВыберите валюту для пополнения:",
        "en": "📥 <b>Deposit</b>\n\nChoose currency to deposit:",
    },
    "deposit_address_ton": {
        "ru": (
            "📥 <b>Пополнение — TON</b>\n\n"
            "💳 <b>Адрес кошелька:</b>\n"
            "<code>{wallet}</code>\n\n"
            "💡 <b>Минимум:</b> {minimum} TON\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📝 В комментарии укажите:\n"
            "<code>DEPOSIT_{user_id}</code>\n\n"
            "⚡ Зачисление: 1–2 минуты"
        ),
        "en": (
            "📥 <b>Deposit — TON</b>\n\n"
            "💳 <b>Wallet address:</b>\n"
            "<code>{wallet}</code>\n\n"
            "💡 <b>Minimum:</b> {minimum} TON\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📝 In memo/comment write:\n"
            "<code>DEPOSIT_{user_id}</code>\n\n"
            "⚡ Credited in 1–2 minutes"
        ),
    },
    "deposit_address_usdt": {
        "ru": (
            "📥 <b>Пополнение — USDT (TRC-20)</b>\n\n"
            "💳 <b>Адрес кошелька:</b>\n"
            "<code>{wallet}</code>\n\n"
            "💡 <b>Минимум:</b> {minimum} USDT\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ <b>Сеть: TRC-20 (Tron)</b>\n"
            "Не отправляйте через другие сети!\n\n"
            "⚡ Зачисление: 1–2 минуты"
        ),
        "en": (
            "📥 <b>Deposit — USDT (TRC-20)</b>\n\n"
            "💳 <b>Wallet address:</b>\n"
            "<code>{wallet}</code>\n\n"
            "💡 <b>Minimum:</b> {minimum} USDT\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⚠️ <b>Network: TRC-20 (Tron)</b>\n"
            "Do NOT send via other networks!\n\n"
            "⚡ Credited in 1–2 minutes"
        ),
    },
    "deposit_enter_amount": {
        "ru": "💬 Введите сумму в <b>{currency}</b>:\n<i>Пример: 100</i>",
        "en": "💬 Enter amount in <b>{currency}</b>:\n<i>Example: 100</i>",
    },
    "deposit_too_small": {
        "ru": "❌ Минимальная сумма: <b>{minimum} {currency}</b>",
        "en": "❌ Minimum amount: <b>{minimum} {currency}</b>",
    },
    "deposit_pending": {
        "ru": (
            "✅ <b>Ожидаем пополнения</b>\n\n"
            "💰 Сумма: <code>{amount:.2f} {currency}</code>\n\n"
            "📝 Укажите в комментарии:\n"
            "<code>DEPOSIT_{user_id}</code>\n\n"
            "⏱ Зачисление: 1–2 минуты автоматически"
        ),
        "en": (
            "✅ <b>Awaiting deposit</b>\n\n"
            "💰 Amount: <code>{amount:.2f} {currency}</code>\n\n"
            "📝 Write in memo/comment:\n"
            "<code>DEPOSIT_{user_id}</code>\n\n"
            "⏱ Auto-credited in 1–2 minutes"
        ),
    },

    # ──────────────── WITHDRAW ────────────────
    "withdraw_choose": {
        "ru": "📤 <b>Вывод средств</b>\n\nВыберите валюту:",
        "en": "📤 <b>Withdrawal</b>\n\nChoose currency:",
    },
    "withdraw_enter_amount": {
        "ru": (
            "💵 <b>Баланс:</b> <code>{balance:.4f} {currency}</code>\n"
            "💡 <b>Минимум:</b> {minimum} {currency}\n\n"
            "Введите сумму для вывода:"
        ),
        "en": (
            "💵 <b>Balance:</b> <code>{balance:.4f} {currency}</code>\n"
            "💡 <b>Minimum:</b> {minimum} {currency}\n\n"
            "Enter withdrawal amount:"
        ),
    },
    "withdraw_enter_address_ton": {
        "ru": "📬 Введите ваш <b>TON-адрес</b> (начинается с UQ или EQ):",
        "en": "📬 Enter your <b>TON address</b> (starts with UQ or EQ):",
    },
    "withdraw_enter_address_usdt": {
        "ru": "📬 Введите ваш <b>USDT TRC-20 адрес</b> (начинается с T):",
        "en": "📬 Enter your <b>USDT TRC-20 address</b> (starts with T):",
    },
    "withdraw_bad_amount": {
        "ru": "❌ Введите корректную сумму.",
        "en": "❌ Enter a valid amount.",
    },
    "withdraw_too_small": {
        "ru": "❌ Минимальная сумма вывода: <b>{minimum} {currency}</b>",
        "en": "❌ Minimum withdrawal: <b>{minimum} {currency}</b>",
    },
    "withdraw_insufficient": {
        "ru": "❌ Недостаточно средств.\n💵 Баланс: <code>{balance:.4f} {currency}</code>",
        "en": "❌ Insufficient funds.\n💵 Balance: <code>{balance:.4f} {currency}</code>",
    },
    "withdraw_bad_ton_addr": {
        "ru": "❌ Некорректный TON-адрес. Должен начинаться с <b>UQ</b> или <b>EQ</b>.",
        "en": "❌ Invalid TON address. Must start with <b>UQ</b> or <b>EQ</b>.",
    },
    "withdraw_bad_usdt_addr": {
        "ru": "❌ Некорректный TRC-20 адрес. Должен начинаться с <b>T</b>.",
        "en": "❌ Invalid TRC-20 address. Must start with <b>T</b>.",
    },
    "withdraw_created": {
        "ru": (
            "✅ <b>Заявка на вывод создана!</b>\n\n"
            "💰 Сумма: <code>{amount:.2f} {currency}</code>\n"
            "📋 Номер заявки: <b>#{wid}</b>\n\n"
            "⏳ Обрабатывается в течение 24 часов"
        ),
        "en": (
            "✅ <b>Withdrawal request created!</b>\n\n"
            "💰 Amount: <code>{amount:.2f} {currency}</code>\n"
            "📋 Request #: <b>#{wid}</b>\n\n"
            "⏳ Processed within 24 hours"
        ),
    },

    # ──────────────── STATS ────────────────
    "stats": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   📊 <b>СТАТИСТИКА</b>       ║\n"
            "╚═══════════════════════╝\n\n"
            "💵 <b>Баланс USDT:</b>  <code>{usdt:.2f}</code>\n"
            "💎 <b>Баланс TON:</b>   <code>{ton:.4f}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📈 <b>Дневная доходность:</b> {pct}%\n"
            "  • ~<code>{daily_usdt:.4f}</code> USDT / день\n"
            "  • ~<code>{daily_ton:.6f}</code> TON / день\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💼 <b>Внесено всего:</b>\n"
            "  • USDT: <code>{dep_usdt:.2f}</code>\n"
            "  • TON:  <code>{dep_ton:.4f}</code>\n\n"
            "🔒 <b>В стейкинге:</b> <code>{staked:.2f}</code> USDT\n"
            "🤝 <b>Реф. доход:</b>  <code>{ref_earn:.2f}</code> USDT"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   📊 <b>STATISTICS</b>       ║\n"
            "╚═══════════════════════╝\n\n"
            "💵 <b>USDT Balance:</b>  <code>{usdt:.2f}</code>\n"
            "💎 <b>TON Balance:</b>   <code>{ton:.4f}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📈 <b>Daily yield:</b> {pct}%\n"
            "  • ~<code>{daily_usdt:.4f}</code> USDT / day\n"
            "  • ~<code>{daily_ton:.6f}</code> TON / day\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💼 <b>Total deposited:</b>\n"
            "  • USDT: <code>{dep_usdt:.2f}</code>\n"
            "  • TON:  <code>{dep_ton:.4f}</code>\n\n"
            "🔒 <b>Staked:</b>        <code>{staked:.2f}</code> USDT\n"
            "🤝 <b>Ref. earnings:</b> <code>{ref_earn:.2f}</code> USDT"
        ),
    },

    # ──────────────── HISTORY ────────────────
    "history_title": {
        "ru": "📋 <b>История операций</b>",
        "en": "📋 <b>Transaction History</b>",
    },
    "history_empty": {
        "ru": "📋 <b>История пуста</b>\n\nОпераций ещё не было.",
        "en": "📋 <b>History is empty</b>\n\nNo transactions yet.",
    },
    "history_page": {
        "ru": "Страница {page}/{total}",
        "en": "Page {page}/{total}",
    },

    # ──────────────── COPY TRADING ────────────────
    "copy_title": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║  📡 <b>КОПИ-ТРЕЙДИНГ</b>    ║\n"
            "╚═══════════════════════╝\n\n"
            "Копируйте сделки лучших трейдеров\n"
            "и зарабатывайте вместе с ними!\n\n"
            "Выберите раздел:"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║  📡 <b>COPY TRADING</b>     ║\n"
            "╚═══════════════════════╝\n\n"
            "Copy trades of top traders\n"
            "and earn together with them!\n\n"
            "Choose a section:"
        ),
    },
    "copy_traders_list": {
        "ru": "📡 <b>Топ трейдеры</b>\n\nВыберите трейдера для копирования:",
        "en": "📡 <b>Top Traders</b>\n\nSelect a trader to copy:",
    },
    "copy_trader_card": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║  👤 <b>{name}</b> {flag}       ║\n"
            "╚═══════════════════════╝\n\n"
            "📊 <b>Сделки:</b> {win}/{total} (побед)\n"
            "🎯 <b>Винрейт:</b> {winrate:.1f}%\n"
            "📈 <b>Доход / мес:</b> +{monthly:.1f}%\n"
            "👥 <b>Подписчиков:</b> {followers}\n"
            "⚡ <b>Риск:</b> {risk}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📋 <b>Стратегия:</b>\n{strategy}\n\n"
            "Введите сумму USDT для копирования:"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║  👤 <b>{name}</b> {flag}       ║\n"
            "╚═══════════════════════╝\n\n"
            "📊 <b>Trades:</b> {win}/{total} (wins)\n"
            "🎯 <b>Win rate:</b> {winrate:.1f}%\n"
            "📈 <b>Monthly yield:</b> +{monthly:.1f}%\n"
            "👥 <b>Followers:</b> {followers}\n"
            "⚡ <b>Risk:</b> {risk}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📋 <b>Strategy:</b>\n{strategy}\n\n"
            "Enter USDT amount to copy:"
        ),
    },
    "copy_opened": {
        "ru": (
            "✅ <b>Копирование запущено!</b>\n\n"
            "👤 Трейдер: <b>{trader}</b>\n"
            "💰 Сумма: <code>{amount:.2f} USDT</code>\n\n"
            "📊 Прибыль начисляется вместе с ежедневными выплатами."
        ),
        "en": (
            "✅ <b>Copy trading started!</b>\n\n"
            "👤 Trader: <b>{trader}</b>\n"
            "💰 Amount: <code>{amount:.2f} USDT</code>\n\n"
            "📊 Profit is credited with daily payouts."
        ),
    },
    "copy_my_positions": {
        "ru": "📡 <b>Мои позиции копитрейдинга</b>",
        "en": "📡 <b>My Copy Trading Positions</b>",
    },
    "copy_no_positions": {
        "ru": "У вас нет активных позиций копитрейдинга.",
        "en": "You have no active copy trading positions.",
    },
    "copy_position_item": {
        "ru": (
            "👤 <b>{trader}</b> | 💰 <code>{amount:.2f} USDT</code>\n"
            "📅 Открыта: {date} | 💹 Заработано: <code>{earned:.4f}</code>"
        ),
        "en": (
            "👤 <b>{trader}</b> | 💰 <code>{amount:.2f} USDT</code>\n"
            "📅 Opened: {date} | 💹 Earned: <code>{earned:.4f}</code>"
        ),
    },
    "copy_closed": {
        "ru": "✅ Позиция закрыта. Средства возвращены на баланс.",
        "en": "✅ Position closed. Funds returned to balance.",
    },
    "copy_insufficient": {
        "ru": "❌ Недостаточно USDT на балансе.",
        "en": "❌ Insufficient USDT balance.",
    },

    # ──────────────── STAKING ────────────────
    "staking_title": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   🏦 <b>СТЕЙКИНГ</b>        ║\n"
            "╚═══════════════════════╝\n\n"
            "Заблокируйте средства и получайте\n"
            "повышенную доходность!\n\n"
            "Выберите план:"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   🏦 <b>STAKING</b>         ║\n"
            "╚═══════════════════════╝\n\n"
            "Lock your funds and earn\n"
            "higher yield!\n\n"
            "Choose a plan:"
        ),
    },
    "staking_plan_info": {
        "ru": (
            "{emoji} <b>{name}</b>\n\n"
            "📈 Доходность: <b>{pct}% / день</b>\n"
            "💡 Минимум: <b>{min_usdt} USDT</b>\n"
            "🔒 Блокировка: <b>{lock}</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💵 Ваш баланс: <code>{balance:.2f}</code> USDT\n\n"
            "Введите сумму для стейкинга:"
        ),
        "en": (
            "{emoji} <b>{name}</b>\n\n"
            "📈 Yield: <b>{pct}% / day</b>\n"
            "💡 Minimum: <b>{min_usdt} USDT</b>\n"
            "🔒 Lock: <b>{lock}</b>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💵 Your balance: <code>{balance:.2f}</code> USDT\n\n"
            "Enter staking amount:"
        ),
    },
    "staking_opened": {
        "ru": (
            "✅ <b>Стейкинг активирован!</b>\n\n"
            "{emoji} План: <b>{name}</b>\n"
            "💰 Сумма: <code>{amount:.2f} USDT</code>\n"
            "📈 Доходность: <b>{pct}%/день</b>\n"
            "🔓 Разблокировка: <b>{unlock}</b>"
        ),
        "en": (
            "✅ <b>Staking activated!</b>\n\n"
            "{emoji} Plan: <b>{name}</b>\n"
            "💰 Amount: <code>{amount:.2f} USDT</code>\n"
            "📈 Yield: <b>{pct}%/day</b>\n"
            "🔓 Unlock: <b>{unlock}</b>"
        ),
    },
    "staking_insufficient": {
        "ru": "❌ Недостаточно USDT. Минимум: <b>{min_usdt}</b>",
        "en": "❌ Insufficient USDT. Minimum: <b>{min_usdt}</b>",
    },
    "staking_my_title": {
        "ru": "🏦 <b>Мои стейкинг-позиции</b>",
        "en": "🏦 <b>My Staking Positions</b>",
    },
    "staking_no_positions": {
        "ru": "У вас нет активных стейкинг-позиций.",
        "en": "You have no active staking positions.",
    },
    "staking_position_item": {
        "ru": (
            "{emoji} <b>{name}</b> | <code>{amount:.2f} USDT</code>\n"
            "📈 {pct}%/д | 🔓 {unlock} | 💹 Заработано: <code>{earned:.4f}</code>"
        ),
        "en": (
            "{emoji} <b>{name}</b> | <code>{amount:.2f} USDT</code>\n"
            "📈 {pct}%/d | 🔓 {unlock} | 💹 Earned: <code>{earned:.4f}</code>"
        ),
    },
    "staking_locked": {
        "ru": "🔒 Позиция заблокирована до {date}",
        "en": "🔒 Position locked until {date}",
    },
    "staking_closed": {
        "ru": "✅ Стейкинг закрыт. Средства возвращены на баланс.",
        "en": "✅ Staking closed. Funds returned to balance.",
    },

    # ──────────────── REFERRAL ────────────────
    "referral_title": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║  🤝 <b>РЕФЕРАЛЫ</b>         ║\n"
            "╚═══════════════════════╝\n\n"
            "🔗 <b>Ваша реферальная ссылка:</b>\n"
            "<code>{link}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎁 Бонус: <b>{pct}%</b> от первого депозита реферала\n\n"
            "👥 <b>Приглашено:</b> {count} чел.\n"
            "💰 <b>Заработано:</b> <code>{earned:.2f}</code> USDT"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║  🤝 <b>REFERRALS</b>        ║\n"
            "╚═══════════════════════╝\n\n"
            "🔗 <b>Your referral link:</b>\n"
            "<code>{link}</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🎁 Bonus: <b>{pct}%</b> of referee's first deposit\n\n"
            "👥 <b>Invited:</b> {count} people\n"
            "💰 <b>Earned:</b> <code>{earned:.2f}</code> USDT"
        ),
    },

    # ──────────────── SUPPORT ────────────────
    "support": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   🆘 <b>ПОДДЕРЖКА</b>       ║\n"
            "╚═══════════════════════╝\n\n"
            "По всем вопросам:\n"
            "👤 {support}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Время ответа: до 2 часов\n"
            "🌐 Режим работы: 24/7"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   🆘 <b>SUPPORT</b>         ║\n"
            "╚═══════════════════════╝\n\n"
            "For any questions:\n"
            "👤 {support}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "⏰ Response time: up to 2 hours\n"
            "🌐 Working hours: 24/7"
        ),
    },

    # ──────────────── HELP ────────────────
    "help": {
        "ru": (
            "╔═══════════════════════╗\n"
            "║   ❓ <b>ПОМОЩЬ</b>          ║\n"
            "╚═══════════════════════╝\n\n"
            "💡 <b>Как это работает?</b>\n"
            "Ваши средства работают на платформе\n"
            "копи-трейдинга. Прибыль начисляется\n"
            "ежедневно в 00:00 UTC.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📥 <b>Пополнение</b>\n"
            "• TON: мин. {min_ton} TON\n"
            "• USDT: мин. {min_usdt} USDT (TRC-20)\n"
            "• Зачисление: 1–2 мин автоматически\n\n"
            "📤 <b>Вывод</b>\n"
            "• TON: мин. {min_w_ton} TON\n"
            "• USDT: мин. {min_w_usdt} USDT\n"
            "• Срок: до 24 часов\n\n"
            "📡 <b>Копитрейдинг</b>\n"
            "Копируйте сделки лучших трейдеров.\n"
            "Прибыль зависит от результатов трейдера.\n\n"
            "🏦 <b>Стейкинг</b>\n"
            "Заблокируйте USDT на срок для повышенного\n"
            "дохода до 4% в день.\n\n"
            "🤝 <b>Рефералы</b>\n"
            "Приглашайте друзей и получайте {ref_pct}%\n"
            "от их первого депозита.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "❓ Вопросы: {support}"
        ),
        "en": (
            "╔═══════════════════════╗\n"
            "║   ❓ <b>HELP</b>            ║\n"
            "╚═══════════════════════╝\n\n"
            "💡 <b>How does it work?</b>\n"
            "Your funds work on the copy-trading\n"
            "platform. Profit is credited daily\n"
            "at 00:00 UTC.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📥 <b>Deposit</b>\n"
            "• TON: min. {min_ton} TON\n"
            "• USDT: min. {min_usdt} USDT (TRC-20)\n"
            "• Credited in 1–2 min automatically\n\n"
            "📤 <b>Withdrawal</b>\n"
            "• TON: min. {min_w_ton} TON\n"
            "• USDT: min. {min_w_usdt} USDT\n"
            "• Duration: up to 24 hours\n\n"
            "📡 <b>Copy Trading</b>\n"
            "Copy trades of top traders.\n"
            "Profit depends on trader's results.\n\n"
            "🏦 <b>Staking</b>\n"
            "Lock USDT for enhanced returns\n"
            "up to 4% per day.\n\n"
            "🤝 <b>Referrals</b>\n"
            "Invite friends and earn {ref_pct}%\n"
            "from their first deposit.\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "❓ Questions: {support}"
        ),
    },

    # ──────────────── LANGUAGE ────────────────
    "language_choose": {
        "ru": "🌐 <b>Выберите язык / Choose language:</b>",
        "en": "🌐 <b>Выберите язык / Choose language:</b>",
    },
    "language_changed_ru": {
        "ru": "✅ Язык изменён на <b>Русский</b> 🇷🇺",
        "en": "✅ Язык изменён на <b>Русский</b> 🇷🇺",
    },
    "language_changed_en": {
        "ru": "✅ Language changed to <b>English</b> 🇬🇧",
        "en": "✅ Language changed to <b>English</b> 🇬🇧",
    },

    # ──────────────── NOTIFICATIONS ────────────────
    "deposit_credited": {
        "ru": (
            "✅ <b>ДЕПОЗИТ ЗАЧИСЛЕН!</b>\n\n"
            "💰 Сумма: <code>{amount:.2f} {currency}</code>\n"
            "💵 Баланс USDT: <code>{usdt:.2f}</code>\n"
            "💎 Баланс TON: <code>{ton:.4f}</code>\n\n"
            "📈 Прибыль начисляется ежедневно в 00:00 UTC\n"
            "🔑 Хэш: <code>{tx_hash}</code>"
        ),
        "en": (
            "✅ <b>DEPOSIT CREDITED!</b>\n\n"
            "💰 Amount: <code>{amount:.2f} {currency}</code>\n"
            "💵 USDT Balance: <code>{usdt:.2f}</code>\n"
            "💎 TON Balance: <code>{ton:.4f}</code>\n\n"
            "📈 Profit is credited daily at 00:00 UTC\n"
            "🔑 Hash: <code>{tx_hash}</code>"
        ),
    },
    "profit_accrued": {
        "ru": (
            "🎉 <b>Ежедневная прибыль начислена!</b>\n\n"
            "{profit_lines}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>Текущий баланс:</b>\n"
            "  • USDT: <code>{usdt:.2f}</code>\n"
            "  • TON:  <code>{ton:.4f}</code>"
        ),
        "en": (
            "🎉 <b>Daily profit accrued!</b>\n\n"
            "{profit_lines}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━\n"
            "📊 <b>Current balance:</b>\n"
            "  • USDT: <code>{usdt:.2f}</code>\n"
            "  • TON:  <code>{ton:.4f}</code>"
        ),
    },

    # ──────────────── COMMON ────────────────
    "invalid_number": {
        "ru": "❌ Неверный формат. Введите число, например: <code>100</code>",
        "en": "❌ Invalid format. Enter a number, e.g.: <code>100</code>",
    },
    "back": {
        "ru": "⬅️ Назад",
        "en": "⬅️ Back",
    },
    "main_menu_btn": {
        "ru": "🏠 Главное меню",
        "en": "🏠 Main Menu",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Get translated text for key in given language."""
    block = TEXTS.get(key, {})
    text = block.get(lang, block.get("ru", f"[missing: {key}]"))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text
