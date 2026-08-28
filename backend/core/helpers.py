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


# def calculate_volatility(returns):
#     return (
#         np.std(returns, ddof=1)
#         * np.sqrt(12)
#     )


# def calculate_max_drawdown(returns):
#     value = 1.0
#     peak = 1.0
#     max_drawdown = 0.0
#     for r in returns:
#         value *= (1 + r)
#         if value > peak:
#             peak = value
#         drawdown = (
#             value / peak
#         ) - 1
#         max_drawdown = min(
#             max_drawdown,
#             drawdown
#         )
#     return max_drawdown


# def evaluate_fund(fund_rows, mandate):
#     """
#     System evaluates fund deterministically.
#     """

#     # Each fund_rows contains all monthly observations
#     # for one fund.
#     fund = fund_rows[0]
#     returns = [
#         row["monthly_return"]
#         for row in fund_rows
#     ]
#     # CALCULATE FUND METRICS
#     volatility = calculate_volatility(
#         returns
#     )
#     max_drawdown = calculate_max_drawdown(
#         returns
#     )
#     # LIQUIDITY CHECK
#     if mandate["liquidity"] == "No preference":

#         liquidity_pass = True
#     else:
#         fund_liquidity = LIQUIDITY_ORDER[
#             fund["redemption_frequency"]
#         ]

#         required_liquidity = LIQUIDITY_ORDER[
#             mandate["liquidity"]
#         ]

#         liquidity_pass = (
#             fund_liquidity
#             <= required_liquidity
#         )
#     # VOLATILITY CHECK
#     min_vol, max_vol = VOLATILITY_RULES[
#         mandate["target_volatility"]
#     ]
#     if min_vol is None:
#         volatility_pass = True
#     elif max_vol is None:
#         volatility_pass = (
#             volatility >= min_vol
#         )
#     else:
#         volatility_pass = (
#             min_vol
#             <= volatility
#             <= max_vol
#         )
#     # DRAWDOWN CHECK
#     max_allowed_drawdown = (
#         DRAWDOWN_RULES[
#             mandate["max_drawdown"]
#         ]
#     )
#     if max_allowed_drawdown is None:
#         drawdown_pass = True
#     else:
#         drawdown_pass = (
#             abs(max_drawdown)
#             <= max_allowed_drawdown
#         )
#     # STRATEGY CHECK
#     strategy_pass = (
#         fund["strategy"]
#         in mandate["strategies"]
#     )
#     # STORE ALL CHECKS
#     checks = {
#         "liquidity": {
#             "value": fund[
#                 "redemption_frequency"
#             ],
#             "pass": liquidity_pass,
#         },
#         "volatility": {
#             "value": round(
#                 float(volatility),
#                 4
#             ),
#             "pass": volatility_pass,
#         },
#         "max_drawdown": {
#             "value": round(
#                 float(max_drawdown),
#                 4
#             ),
#             "pass": drawdown_pass,
#         },
#         "strategy": {
#             "value": fund["strategy"],
#             "pass": strategy_pass,
#         },
#     }
#     # HARD FILTER RESULT
#     eligible = all(
#         check["pass"]
#         for check in checks.values()
#     )
#     return {
#         "fund_id": fund["fund_id"],
#         "eligible": eligible,
#         "checks": checks,
#     }


# def calculate_benchmark_comparison(
#     fund_rows,
#     benchmark_returns,
#     risk_free_rate=0.04,
# ):
#     # 1. Convert fund rows to DataFrame
#     fund_df = pd.DataFrame(fund_rows)

#     # 2. Convert date column to datetime
#     fund_df["date"] = pd.to_datetime(
#         fund_df["date"]
#     )

#     # 3. Check for duplicate dates
#     if fund_df["date"].duplicated().any():
#         duplicates = fund_df.loc[
#             fund_df["date"].duplicated(
#                 keep=False
#             ),
#             "date"
#         ].tolist()
#         raise ValueError(
#             f"Duplicate fund dates found: "
#             f"{duplicates}"
#         )

#     # 4. Set date as index
#     fund_df = fund_df.set_index("date")

#     # 5. Sort dates
#     fund_df = fund_df.sort_index()

#     # 6. Extract fund monthly returns
#     fund_returns = fund_df[
#         "monthly_return"
#     ]

#     # 7. Normalize benchmark index
#     benchmark_returns = benchmark_returns.copy()

#     benchmark_returns.index = pd.to_datetime(
#         benchmark_returns.index
#     )
#     # Remove timezone if it exists
#     if benchmark_returns.index.tz is not None:
#         benchmark_returns.index = (
#             benchmark_returns.index.tz_localize(None)
#         )
#     benchmark_returns = (
#         benchmark_returns.sort_index()
#     )

#     # 8. Align fund and benchmark dates
#     comparison = pd.concat(
#         [
#             fund_returns.rename("fund"),
#             benchmark_returns.rename("benchmark"),
#         ],
#         axis=1,
#         join="inner",
#     )
#     comparison = comparison.dropna()

#     # 9. Check overlapping observations
#     observations = len(comparison)
#     if observations < 2:
#         raise ValueError(
#             "At least 2 overlapping observations "
#             "are required."
#         )

#     # 10. Extract aligned returns
#     fund_returns = comparison["fund"]
#     benchmark_returns = comparison["benchmark"]

#     # 11. Annualized returns
#     fund_cumulative_return = (
#         (1 + fund_returns).prod() - 1
#     )
#     fund_annualized_return = (
#         (1 + fund_cumulative_return)
#         ** (12 / observations)
#         - 1
#     )
#     benchmark_cumulative_return = (
#         (1 + benchmark_returns).prod() - 1
#     )
#     benchmark_annualized_return = (
#         (1 + benchmark_cumulative_return)
#         ** (12 / observations)
#         - 1
#     )

#     # 12. Annualized volatility
#     fund_volatility = (
#         fund_returns.std()
#         * np.sqrt(12)
#     )
#     benchmark_volatility = (
#         benchmark_returns.std()
#         * np.sqrt(12)
#     )

#     # 13. Maximum drawdown helper
#     def calculate_max_drawdown(
#         returns
#     ):
#         cumulative = (
#             1 + returns
#         ).cumprod()
#         running_max = (
#             cumulative.cummax()
#         )
#         drawdown = (
#             cumulative / running_max
#         ) - 1
#         return drawdown.min()

#     # 14. Maximum drawdowns
#     fund_max_drawdown = (
#         calculate_max_drawdown(
#             fund_returns
#         )
#     )
#     benchmark_max_drawdown = (
#         calculate_max_drawdown(
#             benchmark_returns
#         )
#     )

#     # 15. Correlation
#     correlation = fund_returns.corr(
#         benchmark_returns
#     )

#     # 16. Excess return
#     excess_return = (
#         fund_annualized_return
#         - benchmark_annualized_return
#     )

#     # 17. Sharpe ratio
#     if fund_volatility == 0:
#         sharpe_ratio = None
#     else:
#         sharpe_ratio = (
#             fund_annualized_return
#             - risk_free_rate
#         ) / fund_volatility

#     # 18. Return results
#     return {
#         "fund_annualized_return": float(
#             fund_annualized_return
#         ),
#         "benchmark_annualized_return": float(
#             benchmark_annualized_return
#         ),
#         "fund_volatility": float(
#             fund_volatility
#         ),
#         "benchmark_volatility": float(
#             benchmark_volatility
#         ),
#         "fund_max_drawdown": float(
#             fund_max_drawdown
#         ),
#         "benchmark_max_drawdown": float(
#             benchmark_max_drawdown
#         ),
#         "correlation": float(
#             correlation
#         ),
#         "excess_return": float(
#             excess_return
#         ),
#         "sharpe_ratio": (
#             float(sharpe_ratio)
#             if sharpe_ratio is not None
#             else None
#         ),
#         "risk_free_rate": risk_free_rate,
#         "observations": observations,
#     }


# def score_sharpe(sharpe):
#     if sharpe is None:
#         return 0

#     if sharpe >= 1.5:
#         return 100

#     if sharpe >= 1.0:
#         return 80

#     if sharpe >= 0.75:
#         return 60

#     if sharpe >= 0.50:
#         return 40

#     return 20

# def score_excess_return(excess_return):
#     if excess_return >= 0.05:
#         return 100

#     if excess_return >= 0.03:
#         return 80

#     if excess_return >= 0.01:
#         return 60

#     if excess_return >= 0:
#         return 40
#     return 0

# def score_drawdown(max_drawdown):
#     drawdown = abs(max_drawdown)

#     if drawdown <= 0.05:
#         return 100

#     if drawdown <= 0.10:
#         return 80

#     if drawdown <= 0.15:
#         return 60

#     if drawdown <= 0.20:
#         return 40

#     return 20

# def score_fund(
#     evaluation,
#     comparison,
# ):
#     if not evaluation["eligible"]:
#         return None

#     mandate_score = 100
#     sharpe_score = score_sharpe(
#         comparison["sharpe_ratio"]
#     )
#     excess_return_score = score_excess_return(
#         comparison["excess_return"]
#     )
#     drawdown_score = score_drawdown(
#         comparison["fund_max_drawdown"]
#     )
#     overall_score = (
#         mandate_score * 0.40
#         + sharpe_score * 0.25
#         + excess_return_score * 0.15
#         + drawdown_score * 0.20
#     )

#     return {
#         "mandate_score": mandate_score,
#         "sharpe_score": sharpe_score,
#         "excess_return_score": excess_return_score,
#         "drawdown_score": drawdown_score,
#         "overall_score": round(
#             overall_score,
#             2
#         ),
#     }

# def create_rationale(
#     evaluation,
#     comparison,
# ):
#     reasons = []
#     if evaluation["eligible"]:
#         reasons.append(
#             "Meets all mandatory mandate constraints"
#         )
#     sharpe = comparison["sharpe_ratio"]
#     if sharpe is not None:
#         reasons.append(
#             f"Sharpe ratio of {sharpe:.2f}"
#         )
#     excess_return = comparison["excess_return"]
#     reasons.append(
#         f"{excess_return:.1%} annualized "
#         "excess return versus benchmark"
#     )
#     max_drawdown = comparison[
#         "fund_max_drawdown"
#     ]
#     reasons.append(
#         f"{abs(max_drawdown):.1%} "
#         "maximum drawdown"
#     )
#     return reasons


# def build_ranked_shortlist(
#     funds,
#     mandate,
#     benchmark_data,
# ):
#     eligible_funds = []
#     for fund_id, fund_rows in funds.items():
#         # STAGE 1
#         # Evaluate mandate
#         evaluation = evaluate_fund(
#             fund_rows,
#             mandate,
#         )
#         if not evaluation["eligible"]:
#             continue
#         # Get benchmark ticker
#         benchmark_ticker = (
#             fund_rows[0]["benchmark_ticker"]
#         )
#         benchmark_returns = (
#             benchmark_data[benchmark_ticker]
#         )
#         # Calculate performance
#         comparison = (
#             calculate_benchmark_comparison(
#                 fund_rows,
#                 benchmark_returns,
#             )
#         )
#         # STAGE 2
#         # Calculate score
#         score = score_fund(
#             evaluation,
#             comparison,
#         )
#         # STAGE 3
#         # Create rationale
#         rationale = create_rationale(
#             evaluation,
#             comparison,
#         )

#         eligible_funds.append(
#             {
#                 "fund_id": fund_id,
#                 "fund_name": (
#                     fund_rows[0]["fund_name"]
#                 ),
#                 "strategy": (
#                     fund_rows[0]["strategy"]
#                 ),
#                 "score": (
#                     score["overall_score"]
#                 ),
#                 "score_breakdown": score,
#                 "performance": comparison,
#                 "reasons": rationale,
#             }
#         )
#     # Rank
#     ranked_funds = sorted(
#         eligible_funds,
#         key=lambda fund: fund["score"],
#         reverse=True,
#     )
#     # Add rank
#     for index, fund in enumerate(
#         ranked_funds,
#         start=1,
#     ):
#         fund["rank"] = index
#     return ranked_funds