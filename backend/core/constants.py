
REQUIRED_COLUMNS = {
    "fund_id",
    "fund_name",
    "manager_name",
    "strategy",
    "inception_date",
    "aum",
    "management_fee",
    "performance_fee",
    "lockup_months",
    "redemption_frequency",
    "notice_period_days",
    "benchmark_ticker",
    "date",
    "monthly_return",
    "notes",
    "key_risks",
}

MAX_UPLOAD_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


SUPPORTED_DATE_FORMATS = [
    "%m/%d/%y",  # 1/1/18
    "%m/%d/%Y",  # 1/1/2018
    "%m-%d-%y",  # 1-1-18
    "%m-%d-%Y",  # 1-1-2018
    "%Y-%m-%d",  # 2018-01-01
    "%Y/%m/%d",  # 2018/01/01
]

VOLATILITY_RULES = {
    "LOW": (0.00, 0.05),
    "LOW_MODERATE": (0.05, 0.08),
    "MODERATE": (0.08, 0.12),
    "MODERATE_HIGH": (0.12, 0.16),
    "HIGH": (0.16, None),
    "NO_TARGET": (None, None),
}

DRAWDOWN_RULES = {
    "CONSERVATIVE": 0.05,
    "MODERATE": 0.10,
    "ELEVATED": 0.15,
    "AGGRESSIVE": 0.25,
    "NO_LIMIT": None,
}

LIQUIDITY_ORDER = {
    "Daily": 1,
    "Weekly": 2,
    "Monthly": 3,
    "Quarterly": 4,
    "Semi-Annual": 5,
    "Annual": 6,
}
