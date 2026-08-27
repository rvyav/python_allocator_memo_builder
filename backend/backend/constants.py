
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
