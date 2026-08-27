from django.conf import settings
from django.db import connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser

import io
import csv

from .constants import MAX_UPLOAD_FILE_SIZE_BYTES, REQUIRED_COLUMNS
from .helpers import parse_date

@api_view(["GET"])
def health_check(request):
    try:
        connection.ensure_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return Response({
            "message": "connected!!!",
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "message": "disconnected!!!",
            "error": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload(request):
    file_data = request.FILES.get("file")

    # Validate uploaded file
    if not file_data:
        return Response(
            {"error": "A file is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not file_data.name.lower().endswith(".csv"):
        return Response(
            {"error": "Only CSV files are supported."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if file_data.size > MAX_UPLOAD_FILE_SIZE_BYTES:
        return Response(
            {
                "error": "File size must not exceed 10 MB.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Decode CSV
    try:
        decoded_file = file_data.read().decode("utf-8-sig")

    except UnicodeDecodeError:
        return Response(
            {
                "error": "The CSV file must be UTF-8 encoded.",
            },
            status=status.HTTP_400_BAD_REQUEST,
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
                        "The CSV file is empty or "
                        "has no header row."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remove whitespace around column names
        reader.fieldnames = [
            field.strip() if field else field
            for field in reader.fieldnames
        ]

        missing_columns = (
            REQUIRED_COLUMNS - set(reader.fieldnames)
        )

        if missing_columns:
            return Response(
                {
                    "error": "CSV is missing required columns.",
                    "missing_columns": sorted(missing_columns),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        rows = []

        # Process CSV rows
        for row_number, row in enumerate(reader, start=2):
            try:
                # String fields
                fund_id = (row.get("fund_id") or "").strip()
                fund_name = (row.get("fund_name") or "").strip()
                manager_name = (
                    row.get("manager_name") or ""
                ).strip()
                strategy = (row.get("strategy") or "").strip()

                redemption_frequency = (
                    row.get("redemption_frequency") or ""
                ).strip()

                benchmark_ticker = (
                    row.get("benchmark_ticker") or ""
                ).strip()

                notes = (row.get("notes") or "").strip()
                key_risks = (row.get("key_risks") or "").strip()

                # Validate required string fields
                required_fields = {
                    "fund_id": fund_id,
                    "fund_name": fund_name,
                    "manager_name": manager_name,
                    "strategy": strategy,
                    "redemption_frequency": (
                        redemption_frequency
                    ),
                    "benchmark_ticker": benchmark_ticker,
                }

                for field_name, value in required_fields.items():
                    if not value:
                        raise ValueError(
                            f"{field_name} is required."
                        )

                # Dates: Accept multiple formats and
                # normalize to: YYYY-MM-DD
                inception_date = parse_date(
                    row.get("inception_date"),
                    "inception_date",
                )

                date = parse_date(
                    row.get("date"),
                    "date",
                )

                # Numeric fields
                try:
                    aum = int(
                        (row.get("aum") or "").strip()
                    )
                except ValueError:
                    raise ValueError(
                        "aum must be a valid integer."
                    )

                try:
                    management_fee = float(
                        (
                            row.get("management_fee") or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "management_fee must be a valid number."
                    )

                try:
                    performance_fee = float(
                        (
                            row.get("performance_fee") or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "performance_fee must be a valid number."
                    )

                try:
                    monthly_return = float(
                        (
                            row.get("monthly_return") or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "monthly_return must be a valid number."
                    )

                try:
                    lockup_months = int(
                        (
                            row.get("lockup_months") or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "lockup_months must be a valid integer."
                    )

                try:
                    notice_period_days = int(
                        (
                            row.get("notice_period_days") or ""
                        ).strip()
                    )
                except ValueError:
                    raise ValueError(
                        "notice_period_days must be a valid integer."
                    )

                rows.append(
                    {
                        "fund_id": fund_id,
                        "fund_name": fund_name,
                        "manager_name": manager_name,
                        "strategy": strategy,
                        "inception_date": inception_date,
                        "aum": aum,
                        "management_fee": management_fee,
                        "performance_fee": performance_fee,
                        "lockup_months": lockup_months,
                        "redemption_frequency": (
                            redemption_frequency
                        ),
                        "notice_period_days": (
                            notice_period_days
                        ),
                        "benchmark_ticker": benchmark_ticker,
                        "date": date,
                        "monthly_return": monthly_return,
                        "notes": notes,
                        "key_risks": key_risks,
                    }
                )

            except (ValueError, TypeError) as exc:
                return Response(
                    {
                        "error": str(exc),
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

    except csv.Error:
        return Response(
            {
                "error": (
                    "The uploaded file contains "
                    "invalid CSV data."
                ),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            "message": "Uploaded successfully",
            "data": {
                "row_count": len(rows),
                "rows": rows,
            }
        },
        status=status.HTTP_200_OK,
    )
