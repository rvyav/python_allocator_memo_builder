
def build_claims(
    ranked_shortlist,
    funds,
):
    claims = []
    claim_number = 1
    for ranked_fund in ranked_shortlist:
        fund_id = ranked_fund["fund_id"]
        fund = funds[fund_id][0]
        performance = ranked_fund[
            "performance"
        ]

        def add_claim(
            text,
            metric,
            value,
        ):
            nonlocal claim_number
            claims.append({
                "claim_id": (
                    f"CLAIM-{claim_number:03d}"
                ),
                "fund_id": fund_id,
                "text": text,
                "metric": metric,
                "value": value,
            })
            claim_number += 1
        # Rank
        add_claim(
            text=(
                f"{fund['fund_name']} ranks "
                f"#{ranked_fund['rank']}."
            ),
            metric="rank",
            value=ranked_fund["rank"],
        )
        # Score
        add_claim(
            text=(
                f"{fund['fund_name']} has an "
                f"overall score of "
                f"{ranked_fund['score']:.1f}."
            ),
            metric="overall_score",
            value=ranked_fund["score"],
        )
        # Return
        add_claim(
            text=(
                f"{fund['fund_name']} has an "
                f"annualized return of "
                f"{performance['fund_annualized_return']:.1%}."
            ),
            metric="fund_annualized_return",
            value=performance[
                "fund_annualized_return"
            ],
        )
        # Volatility
        add_claim(
            text=(
                f"{fund['fund_name']} has "
                f"annualized volatility of "
                f"{performance['fund_volatility']:.1%}."
            ),
            metric="fund_volatility",
            value=performance[
                "fund_volatility"
            ],
        )
        # Sharpe
        add_claim(
            text=(
                f"{fund['fund_name']} has a "
                f"Sharpe ratio of "
                f"{performance['sharpe_ratio']:.2f}."
            ),
            metric="sharpe_ratio",
            value=performance[
                "sharpe_ratio"
            ],
        )
        # Excess return
        add_claim(
            text=(
                f"{fund['fund_name']} generated "
                f"{performance['excess_return']:.1%} "
                f"annualized excess return "
                f"versus its benchmark."
            ),
            metric="excess_return",
            value=performance[
                "excess_return"
            ],
        )
        # Drawdown
        add_claim(
            text=(
                f"{fund['fund_name']} had a "
                f"maximum drawdown of "
                f"{performance['fund_max_drawdown']:.1%}."
            ),
            metric="fund_max_drawdown",
            value=performance[
                "fund_max_drawdown"
            ],
        )
        # Observations
        add_claim(
            text=(
                "Benchmark-relative metrics are "
                f"based on "
                f"{performance['observations']} "
                "overlapping monthly observations."
            ),
            metric="observations",
            value=performance[
                "observations"
            ],
        )
    return claims
