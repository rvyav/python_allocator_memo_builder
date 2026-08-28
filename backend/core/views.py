from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import io
import csv
import numpy as np
import json

import yfinance as yf

from .constants import (
    MAX_UPLOAD_FILE_SIZE_BYTES,
    REQUIRED_COLUMNS,
)
    
from .helpers import parse_date

from .services.metrics import build_ranked_shortlist
from .services.claims import build_claims
from .services.memos import (
    generate_ic_memo,
    validate_memo_claims,
    build_audit_view,
)


@api_view(["POST"])
@parser_classes([
    MultiPartParser,
    FormParser
])
def upload(request):
    file_data = request.FILES.get("file")
    mandate = request.data.get("document_preferences")
    print("file mandate ===> ", mandate)
    filename = (
        file_data.name
        if file_data
        else None
    )
    print("filename ===============>", filename)

    # Parse mandate
    if isinstance(mandate, str):
        mandate = json.loads(mandate)

    # Validate uploaded file
    if not file_data:
        return Response(
            {
                "error": (
                    "A file is required."
                )
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )

    if not file_data.name.lower().endswith(".csv"):
        return Response(
            {
                "error": (
                    "Only CSV files "
                    "are supported."
                )
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )

    if (file_data.size > MAX_UPLOAD_FILE_SIZE_BYTES):
        return Response(
            {
                "error": (
                    "File size must not "
                    "exceed 10 MB."
                ),
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )

    # Decode CSV
    try:

        decoded_file = (
            file_data
            .read()
            .decode("utf-8-sig")
        )
    except UnicodeDecodeError:
        return Response(
            {
                "error": (
                    "The CSV file must "
                    "be UTF-8 encoded."
                ),
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )

    # Parse CSV
    try:
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        # Validate headers
        if not reader.fieldnames:
            return Response(
                {
                    "error": (
                        "The CSV file is empty "
                        "or has no header row."
                    ),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )
        reader.fieldnames = [
            field.strip()
            if field
            else field

            for field
            in reader.fieldnames
        ]

        missing_columns = (
            REQUIRED_COLUMNS
            - set(
                reader.fieldnames
            )
        )

        if missing_columns:
            return Response(
                {
                    "error": (
                        "CSV is missing "
                        "required columns."
                    ),
                    "missing_columns": sorted(
                        missing_columns
                    ),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )
        rows = []

        # Process rows
        for row_number, row in enumerate(
            reader,
            start=2
        ):
            try:
                # Strings
                fund_id = (row.get("fund_id") or "").strip()
                fund_name = (row.get("fund_name") or "").strip()
                manager_name = (row.get("manager_name") or "").strip()
                strategy = (row.get("strategy") or "").strip()
                redemption_frequency = (row.get("redemption_frequency") or "").strip()
                benchmark_ticker = (row.get("benchmark_ticker") or "").strip().upper()
                notes = (row.get("notes") or "").strip()
                key_risks = (row.get("key_risks") or "").strip()
                required_fields = {
                    "fund_id": fund_id,
                    "fund_name": fund_name,
                    "manager_name": manager_name,
                    "strategy": strategy,
                    "redemption_frequency": redemption_frequency,
                    "benchmark_ticker": benchmark_ticker,
                }
                for (field_name, value) in required_fields.items():
                    if not value:
                        raise ValueError(f"{field_name} is required.")

                # Dates
                inception_date = parse_date(row.get("inception_date"), "inception_date")
                date = parse_date(row.get("date"), "date")

                # Numeric fields
                try:
                    aum = int((row.get("aum") or "").strip())
                except ValueError:
                    raise ValueError(
                        "aum must be a "
                        "valid integer."
                    )
                try:
                    management_fee = float((row.get("management_fee") or "").strip())
                except ValueError:
                    raise ValueError(
                        "management_fee must "
                        "be a valid number."
                    )
                try:
                    performance_fee = float((row.get("performance_fee") or "").strip())
                except ValueError:
                    raise ValueError(
                        "performance_fee must "
                        "be a valid number."
                    )

                try:
                    monthly_return = float((row.get("monthly_return") or "").strip())
                except ValueError:
                    raise ValueError(
                        "monthly_return must "
                        "be a valid number."
                    )

                try:
                    lockup_months = int(
                        (
                            row.get(
                                "lockup_months"
                            )
                            or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "lockup_months must "
                        "be a valid integer."
                    )

                try:
                    notice_period_days = int((row.get("notice_period_days") or "").strip())
                except ValueError:
                    raise ValueError(
                        "notice_period_days "
                        "must be a valid integer."
                    )

                # Store normalized row
                rows.append({
                    "fund_id": fund_id,
                    "fund_name": fund_name,
                    "manager_name": manager_name,
                    "strategy": strategy,
                    "inception_date": inception_date,
                    "aum": aum,
                    "management_fee": management_fee,
                    "performance_fee": performance_fee,
                    "lockup_months": lockup_months,
                    "redemption_frequency": redemption_frequency,
                    "notice_period_days": notice_period_days,
                    "benchmark_ticker": benchmark_ticker,
                    "date": date,
                    "monthly_return": monthly_return,
                    "notes": notes,
                    "key_risks": key_risks,
                })
            except (ValueError, TypeError) as exc:
                return Response(
                    {
                        "error": str(
                            exc
                        ),
                    },
                    status=(
                        status.HTTP_400_BAD_REQUEST
                    ),
                )
    except csv.Error:
        return Response(
            {
                "error": (
                    "The uploaded file contains "
                    "invalid CSV data."
                ),
            },
            status=(
                status.HTTP_400_BAD_REQUEST
            ),
        )

    # ANALYSIS PIPELINE
    from collections import defaultdict
    from pprint import pprint

    # Group rows by fund
    funds = defaultdict(list)

    for row in rows:
        funds[row["fund_id"]].append(row)

    print("************* FUNDS *************")

    pprint(dict(funds))

    # Benchmark data
    benchmark_data = {}
    benchmark_tickers = { row["benchmark_ticker"] for row in rows }

    for ticker_symbol in benchmark_tickers:
        ticker = yf.Ticker(
            ticker_symbol
        )
        history = ticker.history(
            start="2025-01-01",
            end="2025-04-01",
        )
        monthly_prices = (
            history["Close"]
            .resample("ME")
            .last()
        )
        benchmark_returns = (
            monthly_prices
            .pct_change()
            .dropna()
        )
        benchmark_returns.index = (
            benchmark_returns
            .index
            .tz_localize(None)
        )
        benchmark_data[
            ticker_symbol
        ] = benchmark_returns

    print("************* BENCHMARK DATA *************")

    pprint(benchmark_data.keys())

    # Rank funds
    print("************* RANKING *************")

    ranked_shortlist = (
        build_ranked_shortlist(
            funds,
            mandate,
            benchmark_data,
        )
    )

    pprint(ranked_shortlist)

    # Build deterministic claims
    print("************* BUILD CLAIMS *************")

    claims = build_claims(
        ranked_shortlist,
        funds,
    )

    pprint(claims)

    # ACTION 1:
    # GENERATE IC MEMO

    print("************* GENERATE IC MEMO *************")

    try:
        memo = generate_ic_memo(claims)
    except Exception as exc:
        print(
            "OpenAI memo generation "
            "failed:",
            exc
        )
        return Response(
            {
                "error": (
                    "Failed to generate "
                    "IC memo."
                ),

                "details": str(
                    exc
                ),
            },
            status=(
                status.HTTP_502_BAD_GATEWAY
            ),
        )
    pprint(memo)

    # VALIDATE CLAIM IDs
    invalid_claim_ids = validate_memo_claims(memo, claims)

    if invalid_claim_ids:
        return Response(
            {
                "error": (
                    "Generated memo "
                    "referenced invalid claims."
                ),
                "invalid_claim_ids": (
                    invalid_claim_ids
                ),
            },
            status=(
                status.HTTP_500_INTERNAL_SERVER_ERROR
            ),
        )

    # ACTION 2:
    # BUILD AUDIT VIEW
    print("************* BUILD AUDIT VIEW *************")
    audit = build_audit_view(memo, claims)

    pprint(audit)

    return Response(
        {
            "message": "Analysis completed successfully",
            "data": {
                "filename": filename,
                "row_count": len(rows),
                "rows": rows,
                "ranked_shortlist": ranked_shortlist,
                "claims": claims,
                "memo": memo,
                "audit": audit,
            },
        },
        status=(
            status.HTTP_200_OK
        ),
    )
