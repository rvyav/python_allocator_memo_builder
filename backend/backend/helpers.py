from datetime import datetime

from .constants import SUPPORTED_DATE_FORMATS

def parse_date(value, field_name):
    """
    Parse a date from one of the supported input formats
    and return it as YYYY-MM-DD.
    """
    value = (value or "").strip()

    if not value:
        raise ValueError(f"{field_name} is required.")

    for date_format in SUPPORTED_DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(
                value,
                date_format,
            ).date()

            return parsed_date.isoformat()

        except ValueError:
            continue

    raise ValueError(
        f"{field_name} has an unsupported date format: '{value}'."
    )
