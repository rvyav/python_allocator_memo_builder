
def build_claims(ranked_shortlist):
    claims = []

    claim_number = 1
    for ranked_fund in (ranked_shortlist):
        fund_id = (ranked_fund["fund_id"])
        fund_name = (ranked_fund["fund_name"])
        performance = (ranked_fund["performance"])

        def add_claim(
            text,
            metric,
            value,
        ):
            nonlocal claim_number
            claims.append({
                "claim_id": (
                    f"CLAIM-"
                    f"{claim_number:03d}"
                ),
                "fund_id": fund_id,
                "text": text,
                "metric": metric,
                "value": value,
            })
            claim_number += 1

        # Ranking
        add_claim(
            text=(
                f"{fund_name} ranks "
                f"#{ranked_fund['rank']}."
            ),
            metric="rank",
            value=(ranked_fund["rank"]),
        )

        # Score
        add_claim(
            text=(
                f"{fund_name} has an "
                f"overall score of "
                f"{ranked_fund['score']:.1f}."
            ),
            metric="overall_score",
            value=ranked_fund["score"],
        )

        # Strategy
        add_claim(
            text=(
                f"{fund_name} uses the "
                f"{ranked_fund['strategy']} "
                "strategy."
            ),
            metric="strategy",
            value=(ranked_fund["strategy"]
            ),
        )

        # Benchmark
        add_claim(
            text=(
                f"{fund_name} is compared "
                f"against "
                f"{ranked_fund['benchmark_ticker']}."
            ),
            metric="benchmark_ticker",
            value=ranked_fund["benchmark_ticker"],
        )

        # Return
        add_claim(
            text=(
                f"{fund_name} has an "
                f"annualized return of "
                f"{performance['fund_annualized_return']:.1%}."
            ),
            metric="fund_annualized_return",
            value=performance["fund_annualized_return"],
        )


        # Volatility
        add_claim(
            text=(
                f"{fund_name} has "
                "annualized volatility of "
                f"{performance['fund_volatility']:.1%}."
            ),
            metric="fund_volatility",
            value=performance["fund_volatility"],
        )

        # Sharpe
        sharpe = performance["sharpe_ratio"]

        if sharpe is not None:
            add_claim(
                text=(
                    f"{fund_name} has a "
                    "Sharpe ratio of "
                    f"{sharpe:.2f}."
                ),
                metric="sharpe_ratio",
                value=sharpe,
            )

        # Excess return
        add_claim(
            text=(
                f"{fund_name} generated "
                f"{performance['excess_return']:.1%} "
                "annualized excess return "
                "versus its benchmark."
            ),
            metric="excess_return",
            value=performance["excess_return"],
        )

        # Drawdown
        add_claim(
            text=(
                f"{fund_name} had a "
                "maximum drawdown of "
                f"{performance['fund_max_drawdown']:.1%}."
            ),
            metric="fund_max_drawdown",
            value=performance["fund_max_drawdown"],
        )

        # Observations
        add_claim(
            text=(
                f"Benchmark-relative metrics "
                f"for {fund_name} are based "
                f"on "
                f"{performance['observations']} "
                "overlapping monthly "
                "observations."
            ),
            metric="observations",
            value=performance["observations"],
        )

        # Key risk from CSV
        if ranked_fund.get("key_risks"):
            add_claim(
                text=(
                    f"The source data identifies "
                    f"{ranked_fund['key_risks']} "
                    f"for {fund_name}."
                ),
                metric="key_risks",
                value=(ranked_fund["key_risks"]),
            )
    return claims
