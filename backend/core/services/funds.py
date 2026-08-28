from collections import defaultdict

from ..constants import FUND_METADATA_FIELDS


def group_funds(rows):
    """
    Convert flat CSV rows into:
    {
        "F001": [row, row, row],
        "F002": [row, row, row],
    }
    """
    funds = defaultdict(list)
    for row in rows:
        funds[row["fund_id"]].append(row)
    return dict(funds)


def build_fund_profile(fund_rows):
    """
    Build ONE fund-level metadata object from
    all monthly rows.

    This function also verifies that the
    fund metadata is consistent across every
    monthly observation.
    """
    if not fund_rows:
        raise ValueError("Fund has no observations.")

    fund_id = fund_rows[0]["fund_id"]
    profile = {}
    for field in FUND_METADATA_FIELDS:
        values = {row[field] for row in fund_rows}
        if len(values) > 1:
            raise ValueError(
                f"Inconsistent '{field}' "
                f"for fund {fund_id}: "
                f"{values}"
            )
        profile[field] = (values.pop())

    profile["monthly_returns"] = [
        {
            "date": row["date"],
            "monthly_return": (
                row["monthly_return"]
            ),
        }
        for row in sorted(
            fund_rows,
            key=lambda row: (
                row["date"]
            ),
        )
    ]

    profile["observation_count"] = len(fund_rows)
    return profile
