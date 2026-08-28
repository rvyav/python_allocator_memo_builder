import numpy as np
import pandas as pd

from ..constants import (
    VOLATILITY_RULES,
    DRAWDOWN_RULES,
    LIQUIDITY_ORDER,
)

from .funds import (
    build_fund_profile,
)

# BASIC FUND METRICS
def calculate_volatility(returns):
    return np.std(returns, ddof=1) * np.sqrt(12)


def calculate_max_drawdown(returns):
    value = 1.0
    peak = 1.0
    max_drawdown = 0.0

    for monthly_return in returns:
        value *= 1 + monthly_return

        if value > peak:
            peak = value

        drawdown = value / peak - 1
        max_drawdown = min(max_drawdown, drawdown)
    return max_drawdown


# STAGE 1
# MANDATE EVALUATION
def evaluate_fund(fund_rows, mandate):
    """
    Evaluate one complete fund group.

    fund_rows contains ALL monthly
    observations for a single fund.
    """
    fund = build_fund_profile(fund_rows)

    returns = [row["monthly_return"] for row in fund_rows]

    # Fund metrics
    volatility = calculate_volatility(returns)
    max_drawdown = calculate_max_drawdown(returns)

    # Liquidity
    if (mandate["liquidity"] == "No preference"):
        liquidity_pass = True
    else:
        fund_liquidity = (
            LIQUIDITY_ORDER[
                fund[
                    "redemption_frequency"
                ]
            ]
        )

        required_liquidity = LIQUIDITY_ORDER[mandate["liquidity"]]
        liquidity_pass = fund_liquidity <= required_liquidity

    # Volatility
    min_vol, max_vol = VOLATILITY_RULES[mandate["target_volatility"]]

    if min_vol is None:
        volatility_pass = True
    elif max_vol is None:
        volatility_pass = volatility >= min_vol
    else:
        volatility_pass = min_vol <= volatility <= max_vol

    # Drawdown
    max_allowed_drawdown = DRAWDOWN_RULES[mandate["max_drawdown"]]

    if (max_allowed_drawdown is None):
        drawdown_pass = True
    else:
        drawdown_pass = abs(max_drawdown) <= max_allowed_drawdown

    # Strategy
    strategy_pass = fund["strategy"] in mandate["strategies"]

    # Checks
    checks = {
        "liquidity": {
            "value": fund["redemption_frequency"],
            "pass": liquidity_pass,
        },

        "volatility": {
            "value": round(float(volatility), 4),
            "pass": volatility_pass,
        },

        "max_drawdown": {
            "value": round(float(max_drawdown), 4),
            "pass": drawdown_pass,
        },

        "strategy": {
            "value": fund["strategy"],
            "pass": strategy_pass,
        },
    }

    eligible = all(check["pass"] for check in checks.values())

    return {
        "fund_id": fund["fund_id"],
        "eligible": eligible,
        "checks": checks,
    }


# BENCHMARK COMPARISON
def calculate_benchmark_comparison(
    fund_rows,
    benchmark_returns,
    risk_free_rate=0.04,
):

    fund_df = pd.DataFrame(fund_rows)
    fund_df["date"] = pd.to_datetime(fund_df["date"])

    # Prevent duplicate months
    if (fund_df["date"].duplicated().any()):
        duplicates = fund_df.loc[fund_df["date"].duplicated(keep=False), "date"].tolist()
        raise ValueError(
            f"Duplicate fund dates found: {duplicates}"
        )

    fund_df = fund_df.set_index("date").sort_index()
    fund_returns = fund_df["monthly_return"]

    benchmark_returns = benchmark_returns.copy()
    benchmark_returns.index = pd.to_datetime(benchmark_returns.index)

    if (benchmark_returns.index.tz is not None):
        benchmark_returns.index = benchmark_returns.index.tz_localize(None)

    benchmark_returns = benchmark_returns.sort_index()


    # Align fund and benchmark
    comparison = pd.concat(
        [fund_returns.rename("fund"), benchmark_returns.rename("benchmark")],
        axis=1,
        join="inner",
    ).dropna()

    observations = len(comparison)
    if observations < 2:
        raise ValueError("At least 2 overlapping observations are required.")

    aligned_fund_returns = comparison["fund"]
    aligned_benchmark_returns = comparison["benchmark"]

    # Annualized fund return
    fund_cumulative_return = (
        (
            1
            + aligned_fund_returns
        ).prod()
        - 1
    )

    fund_annualized_return = (
        (
            1
            + fund_cumulative_return
        )
        ** (
            12 / observations
        )
        - 1
    )

    # Benchmark annualized return
    benchmark_cumulative_return = (
        (
            1
            + aligned_benchmark_returns
        ).prod()
        - 1
    )

    benchmark_annualized_return = (
        (
            1
            + benchmark_cumulative_return
        )
        ** (
            12 / observations
        )
        - 1
    )

    # Volatility
    fund_volatility = aligned_fund_returns.std() * np.sqrt(12)
    benchmark_volatility = aligned_benchmark_returns.std() * np.sqrt(12)

    # Drawdown helper
    def drawdown_from_returns(returns):
        cumulative = (
            1 + returns
        ).cumprod()

        running_max = cumulative.cummax()
        drawdown = (cumulative / running_max) - 1
        return drawdown.min()

    fund_max_drawdown = drawdown_from_returns(aligned_fund_returns)
    benchmark_max_drawdown = drawdown_from_returns(aligned_benchmark_returns)

    # Correlation
    correlation = aligned_fund_returns.corr(aligned_benchmark_returns)

    # Excess return
    excess_return = fund_annualized_return - benchmark_annualized_return

    # Sharpe
    if fund_volatility == 0:
        sharpe_ratio = None
    else:
        sharpe_ratio = (
            (
                fund_annualized_return
                - risk_free_rate
            )
            / fund_volatility
        )

    return {
        "fund_annualized_return": float(fund_annualized_return),
        "benchmark_annualized_return": float(benchmark_annualized_return),
        "fund_volatility": float(fund_volatility),
        "benchmark_volatility": float(benchmark_volatility),
        "fund_max_drawdown": float(fund_max_drawdown),
        "benchmark_max_drawdown": float(benchmark_max_drawdown),
        "correlation": float(correlation),
        "excess_return": float(excess_return),
        "sharpe_ratio": float(sharpe_ratio) if sharpe_ratio is not None else None,
        "risk_free_rate": risk_free_rate,
        "observations": observations,
    }


# SCORING
def score_sharpe(sharpe,):
    if sharpe is None:
        return 0

    if sharpe >= 1.5:
        return 100

    if sharpe >= 1.0:
        return 80

    if sharpe >= 0.75:
        return 60

    if sharpe >= 0.50:
        return 40
    return 20


def score_excess_return(excess_return):
    if excess_return >= 0.05:
        return 100

    if excess_return >= 0.03:
        return 80

    if excess_return >= 0.01:
        return 60

    if excess_return >= 0:
        return 40
    return 0


def score_drawdown(max_drawdown):
    drawdown = abs(max_drawdown)
    if drawdown <= 0.05:
        return 100

    if drawdown <= 0.10:
        return 80

    if drawdown <= 0.15:
        return 60

    if drawdown <= 0.20:
        return 40
    return 20


def score_fund(evaluation, comparison):
    if not evaluation["eligible"]:
        return None

    mandate_score = 100
    sharpe_score = score_sharpe(comparison["sharpe_ratio"])
    excess_return_score = score_excess_return(comparison["excess_return"])
    drawdown_score = score_drawdown(comparison["fund_max_drawdown"])

    overall_score = (
        mandate_score * 0.40
        + sharpe_score * 0.25
        + excess_return_score * 0.15
        + drawdown_score * 0.20
    )

    return {
        "mandate_score": mandate_score,
        "sharpe_score": sharpe_score,
        "excess_return_score": excess_return_score,
        "drawdown_score": drawdown_score,
        "overall_score": round(overall_score, 2),
    }


# RATIONALE
def create_rationale(evaluation, comparison):
    reasons = []

    if evaluation["eligible"]:
        reasons.append("Meets all mandatory mandate constraints")

    sharpe = comparison["sharpe_ratio"]
    if sharpe is not None:
        reasons.append(f"Sharpe ratio of {sharpe:.2f}")

    excess_return = (comparison["excess_return"])
    reasons.append(f"{excess_return:.1%} annualized excess return versus benchmark")
    max_drawdown = (
        comparison[
            "fund_max_drawdown"
        ]
    )

    reasons.append(
        f"{abs(max_drawdown):.1%} "
        "maximum drawdown"
    )
    return reasons


# BUILD RANKED SHORTLIST
def build_ranked_shortlist(
    funds,
    mandate,
    benchmark_data,
):
    eligible_funds = []

    for (fund_id,fund_rows) in funds.items():
        # Build validated fund profile
        fund = build_fund_profile(fund_rows)

        # Stage 1
        # Mandate evaluation
        evaluation = evaluate_fund(fund_rows, mandate)

        if not evaluation["eligible"]:
            continue

        # Fund benchmark
        benchmark_ticker = fund["benchmark_ticker"].strip().upper()

        if (benchmark_ticker not in benchmark_data):
            raise ValueError(
                "Benchmark data "
                "not found for "
                f"{benchmark_ticker}"
            )

        benchmark_returns = benchmark_data[benchmark_ticker]

        # Performance comparison
        comparison = calculate_benchmark_comparison(fund_rows, benchmark_returns)

        # Stage 2
        # Score
        score = score_fund(evaluation, comparison)

        # Stage 3
        # Rationale
        rationale = create_rationale(evaluation, comparison)

        # Save complete ranked object
        eligible_funds.append({
            "fund_id": fund_id,
            "fund_name": fund["fund_name"],
            "manager_name": fund["manager_name"],
            "strategy": fund["strategy"],
            "benchmark_ticker": benchmark_ticker,
            "aum": fund["aum"],
            "management_fee": fund["management_fee"],
            "performance_fee": fund["performance_fee"],
            "lockup_months": fund["lockup_months"],
            "redemption_frequency": fund["redemption_frequency"],
            "notice_period_days": fund["notice_period_days"],
            "notes": fund["notes"],
            "key_risks": fund["key_risks"],
            "score": score["overall_score"],
            "score_breakdown": score,
            "performance": comparison,
            "evaluation": evaluation,
            "reasons": rationale,
        })

    # Sort strongest → weakest
    ranked_funds = sorted(
        eligible_funds,
        key=lambda fund: fund["score"],
        reverse=True,
    )
    # Assign rank
    for index, fund in enumerate(ranked_funds, start=1):
        fund["rank"] = index
    return ranked_funds
