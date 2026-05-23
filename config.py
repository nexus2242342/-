from dataclasses import dataclass

# ─── Staking plans ────────────────────────────────────────
STAKING_PLANS = [
    {
        "id": 1,
        "emoji": "🥉",
        "name_ru": "Базовый",
        "name_en": "Basic",
        "daily_pct": 1.5,
        "min_usdt": 50.0,
        "lock_days": 0,
        "desc_ru": "Без блокировки • выводи когда угодно",
        "desc_en": "No lock • withdraw anytime",
    },
    {
        "id": 2,
        "emoji": "🥈",
        "name_ru": "Стандарт",
        "name_en": "Standard",
        "daily_pct": 2.5,
        "min_usdt": 200.0,
        "lock_days": 7,
        "desc_ru": "Блокировка 7 дней",
        "desc_en": "7-day lock",
    },
    {
        "id": 3,
        "emoji": "🥇",
        "name_ru": "VIP",
        "name_en": "VIP",
        "daily_pct": 4.0,
        "min_usdt": 500.0,
        "lock_days": 30,
        "desc_ru": "Блокировка 30 дней • максимальный доход",
        "desc_en": "30-day lock • maximum yield",
    },
]

# ─── Traders for copy-trading ─────────────────────────────
TRADERS = [
    {
        "id": "alex_pro",
        "name": "Alex Pro",
        "flag": "🇺🇸",
        "win": 847,
        "total": 1000,
        "monthly": 142.3,
        "followers": 2847,
        "strategy_ru": "Скальпинг BTC/ETH на высоких объёмах",
        "strategy_en": "BTC/ETH scalping on high volume",
        "risk": "medium",
    },
    {
        "id": "maria_fx",
        "name": "Maria FX",
        "flag": "🇩🇪",
        "win": 723,
        "total": 900,
        "monthly": 98.7,
        "followers": 1423,
        "strategy_ru": "Долгосрочные позиции по альткоинам",
        "strategy_en": "Long-term altcoin positions",
        "risk": "low",
    },
    {
        "id": "crypto_king",
        "name": "Crypto King",
        "flag": "🇸🇬",
        "win": 612,
        "total": 780,
        "monthly": 87.4,
        "followers": 987,
        "strategy_ru": "Арбитраж и свинг-трейдинг",
        "strategy_en": "Arbitrage and swing trading",
        "risk": "high",
    },
    {
        "id": "trade_master",
        "name": "Trade Master",
        "flag": "🇬🇧",
        "win": 534,
        "total": 680,
        "monthly": 74.2,
        "followers": 642,
        "strategy_ru": "DeFi токены и стейблкоины",
        "strategy_en": "DeFi tokens and stablecoins",
        "risk": "low",
    },
    {
        "id": "night_owl",
        "name": "Night Owl",
        "flag": "🇯🇵",
        "win": 298,
        "total": 370,
        "monthly": 51.8,
        "followers": 381,
        "strategy_ru": "Ночная торговля фьючерсами",
        "strategy_en": "Overnight futures trading",
        "risk": "high",
    },
]


@dataclass
class Config:
    BOT_TOKEN: str            = "8858940438:AAFaR4sEOgxYxq5RG8wgFe_L-6UWq5UOhOk"
    TON_WALLET: str           = "UQDtRwosWY6VfPnwovLRcF2yo46Xv3BcK-mV1Da-1LwbVIaE"
    USDT_WALLET: str          = "TKPuYeveSA2giJV9fFcgbCDsY6abmzMS7Z"
    USDT_CONTRACT: str        = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    MIN_DEPOSIT_TON: float    = 30.0
    MIN_DEPOSIT_USDT: float   = 50.0
    CHECK_INTERVAL: int       = 30
    TX_SCAN_LIMIT: int        = 20
    LOG_CHAT_ID: int          = 8353710361
    SUPPORT_USER: str         = "@MollyWhip1"
    DAILY_PROFIT_PCT: float   = 1.5
    REFERRAL_BONUS_PCT: float = 5.0
    MIN_WITHDRAW_USDT: float  = 50.0
    MIN_WITHDRAW_TON: float   = 10.0
    DB_PATH: str              = "copypulse.db"
    TON_API_URL: str          = "https://toncenter.com/api/v2"
    TRON_API_URL: str         = "https://api.trongrid.io/v1"
    HISTORY_PAGE_SIZE: int    = 8


config = Config()
