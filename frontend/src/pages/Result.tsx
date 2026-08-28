import {
    useSelector,
} from "react-redux";

import {
    useNavigate,
} from "react-router-dom";

import type {
    RootState,
} from "../store/store";

import "./Result.css";


const Result = () => {

    const navigate =
        useNavigate();


    const result =
        useSelector(
            (
                state: RootState
            ) => state.result.result
        );


    if (!result) {

        return (
            <main className="result-page">

                <div className="empty-result">

                    <h1>
                        No analysis available
                    </h1>

                    <p>
                        Generate a memo first.
                    </p>

                    <button
                        onClick={() =>
                            navigate("/")
                        }
                    >
                        Go back
                    </button>

                </div>

            </main>
        );
    }


    const topFund =
        result.ranked_shortlist[0];


    return (
        <main className="result-page">

            <header className="result-header">

                <div>

                    <p className="eyebrow">
                        Investment Committee Analysis
                    </p>

                    <h1>
                        IC Memo
                    </h1>

                    <p>
                        {result.filename}
                    </p>

                </div>


                <button
                    type="button"

                    onClick={() =>
                        navigate("/")
                    }
                >
                    New analysis
                </button>

            </header>


            {/* =========================
          TOP FUND
      ========================== */}

            {
                topFund && (

                    <section className="fund-summary">

                        <div>

                            <span>
                                Rank
                            </span>

                            <strong>
                                #{topFund.rank}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Fund
                            </span>

                            <strong>
                                {topFund.fund_name}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Strategy
                            </span>

                            <strong>
                                {topFund.strategy}
                            </strong>

                        </div>


                        <div>

                            <span>
                                Score
                            </span>

                            <strong>
                                {topFund.score}
                            </strong>

                        </div>

                    </section>

                )
            }


            {/* =========================
          MEMO
      ========================== */}

            <section className="memo-card">

                <h2>
                    Summary
                </h2>

                <p>
                    {result.memo.summary.text}
                </p>


                <h2>
                    Recommendation
                </h2>

                <p>
                    {
                        result.memo
                            .recommendation
                            .text
                    }
                </p>


                <h2>
                    Key Risks
                </h2>

                <p>
                    {
                        result.memo
                            .key_risks
                            .text
                    }
                </p>


                <h2>
                    Data Appendix
                </h2>

                <div className="appendix">

                    {
                        result.memo
                            .data_appendix
                            .map(
                                (
                                    item,
                                    index
                                ) => (

                                    <div
                                        key={index}
                                        className="appendix-row"
                                    >

                                        <span>
                                            {item.label}
                                        </span>

                                        <strong>
                                            {item.value}
                                        </strong>

                                    </div>

                                )
                            )
                    }

                </div>

            </section>


            {/* =========================
          PERFORMANCE
      ========================== */}

            {
                topFund && (

                    <section className="performance-card">

                        <h2>
                            Computed Metrics
                        </h2>

                        <div className="metrics-grid">

                            <Metric
                                label="Annualized Return"
                                value={
                                    formatPercent(
                                        topFund
                                            .performance
                                            .fund_annualized_return
                                    )
                                }
                            />

                            <Metric
                                label="Volatility"
                                value={
                                    formatPercent(
                                        topFund
                                            .performance
                                            .fund_volatility
                                    )
                                }
                            />

                            <Metric
                                label="Sharpe Ratio"
                                value={
                                    topFund
                                        .performance
                                        .sharpe_ratio
                                        .toFixed(2)
                                }
                            />

                            <Metric
                                label="Excess Return"
                                value={
                                    formatPercent(
                                        topFund
                                            .performance
                                            .excess_return
                                    )
                                }
                            />

                            <Metric
                                label="Maximum Drawdown"
                                value={
                                    formatPercent(
                                        topFund
                                            .performance
                                            .fund_max_drawdown
                                    )
                                }
                            />

                            <Metric
                                label="Observations"
                                value={
                                    String(
                                        topFund
                                            .performance
                                            .observations
                                    )
                                }
                            />

                        </div>

                    </section>

                )
            }


            {/* =========================
          AUDIT VIEW
      ========================== */}

            <section className="audit-card">

                <h2>
                    Audit View
                </h2>

                <p className="audit-description">
                    Memo statements linked to
                    deterministic backend claims.
                </p>


                {
                    result.audit.map(
                        (
                            auditItem,
                            index
                        ) => (

                            <article
                                key={index}
                                className="audit-item"
                            >

                                <h3>
                                    {
                                        formatSectionName(
                                            auditItem.section
                                        )
                                    }
                                </h3>


                                <div className="memo-claim">

                                    <span className="audit-label">
                                        Memo statement
                                    </span>

                                    <p>
                                        {
                                            auditItem.memo_text
                                        }
                                    </p>

                                </div>


                                <div className="supporting-claims">

                                    <span className="audit-label">
                                        Supporting claims
                                    </span>


                                    {
                                        auditItem.claims.map(
                                            (claim) => (

                                                <div
                                                    key={
                                                        claim.claim_id
                                                    }
                                                    className="claim-card"
                                                >

                                                    <div className="claim-header">

                                                        <strong>
                                                            {
                                                                claim.claim_id
                                                            }
                                                        </strong>

                                                        <span>
                                                            {
                                                                claim.metric
                                                            }
                                                        </span>

                                                    </div>


                                                    <p>
                                                        {claim.text}
                                                    </p>


                                                    <div className="claim-value">

                                                        Computed value:

                                                        <strong>
                                                            {" "}
                                                            {
                                                                formatMetricValue(
                                                                    claim.metric,
                                                                    claim.value
                                                                )
                                                            }
                                                        </strong>

                                                    </div>

                                                </div>

                                            )
                                        )
                                    }

                                </div>

                            </article>

                        )
                    )
                }

            </section>

        </main>
    );
};


interface MetricProps {
    label: string;
    value: string;
}


const Metric = ({
    label,
    value,
}: MetricProps) => {

    return (
        <div className="metric">

            <span>
                {label}
            </span>

            <strong>
                {value}
            </strong>

        </div>
    );
};


const formatPercent = (
    value: number
) => {

    return `${(
        value * 100
    ).toFixed(1)}%`;
};


const formatMetricValue = (
    metric: string,
    value: number
) => {

    const percentMetrics = [
        "fund_annualized_return",
        "fund_volatility",
        "excess_return",
        "fund_max_drawdown",
    ];


    if (
        percentMetrics.includes(
            metric
        )
    ) {

        return formatPercent(
            value
        );
    }


    if (
        metric ===
        "sharpe_ratio"
    ) {

        return value.toFixed(
            2
        );
    }


    return String(
        value
    );
};


const formatSectionName = (
    section: string
) => {

    return section
        .replaceAll(
            "_",
            " "
        )
        .replace(
            /\b\w/g,
            (letter) =>
                letter.toUpperCase()
        );
};


export default Result;