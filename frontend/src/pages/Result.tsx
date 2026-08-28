import { useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import type { RootState } from "../store/store";
import type { RankedFund } from "../types/analysis";

import "./Result.css";


const Result = () => {
    const navigate = useNavigate();
    const result = useSelector((state: RootState) => state.result.result);

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
                    <button type="button" onClick={() => navigate("/")}>
                        Go back
                    </button>
                </div>
            </main>
        );
    }

    return (
        <main className="result-page">
            {/* =================================
                HEADER
            ================================== */}
            <header className="result-header">
                <div>
                    <p className="eyebrow">
                        Investment Committee Analysis
                    </p>
                    <h1>IC Memo</h1>
                    <p>File: {result.filename}</p>
                    <p>
                        Funds analyzed:{" "}
                        {
                            result.ranked_shortlist.length
                        }
                    </p>
                </div>
                <button type="button" onClick={() => navigate("/")}>
                    New analysis
                </button>
            </header>

            {/* =================================
                RANKED SHORTLIST
            ================================== */}
            <section className="ranking-card">
                <div className="section-heading">
                    <div>
                        <p className="eyebrow">
                            Deterministic ranking
                        </p>
                        <h2>Ranked Shortlist</h2>
                    </div>
                </div>
                {
                    result.ranked_shortlist.length === 0
                        ? (
                            <p>No funds satisfied the mandate. </p>
                        )
                        : (
                            <div className="ranking-list">
                                {
                                    result.ranked_shortlist.map(
                                        (fund) => (
                                            <RankedFundCard
                                                key={
                                                    fund.fund_id
                                                }
                                                fund={
                                                    fund
                                                }
                                            />
                                        )
                                    )
                                }

                            </div>
                        )
                }
            </section>
            {/* =================================
                IC MEMO
            ================================== */}
            {
                result.memo && (
                    <section className="memo-card">
                        <div className="section-heading">
                            <div>
                                <p className="eyebrow">Generated narrative</p>
                                <h2>Investment Committee Memo</h2>
                            </div>
                        </div>
                        {/* Summary */}
                        <MemoSection
                            title="Summary"
                            text={result.memo.summary.text}
                            claimIds={result.memo.summary.claim_ids}
                        />
                        {/* Recommendation */}
                        <MemoSection
                            title="Recommendation"
                            text={result.memo.recommendation.text}
                            claimIds={result.memo.recommendation.claim_ids}
                        />
                        {/* Key Risks */}
                        <MemoSection
                            title="Key Risks"
                            text={result.memo.key_risks.text}
                            claimIds={result.memo.key_risks.claim_ids}
                        />
                        {/* Data Appendix */}
                        <div className="memo-section">
                            <h3>Data Appendix</h3>
                            <div className="appendix">
                                {
                                    result.memo
                                        .data_appendix
                                        .map((item, index) => (
                                            <div
                                                key={`${item.label}-${index}`}
                                                className="appendix-row"
                                            >
                                                <div>
                                                    <span className="appendix-label">
                                                        {item.label}
                                                    </span>
                                                    <div className="claim-tags">
                                                        {
                                                            item.claim_ids.map((claimId) => (
                                                                <span
                                                                    key={claimId}
                                                                    className="claim-tag"
                                                                >
                                                                    {claimId}
                                                                </span>
                                                            ))
                                                        }
                                                    </div>
                                                </div>

                                                <strong>
                                                    {item.value}
                                                </strong>

                                            </div>

                                        ))
                                }
                            </div>
                        </div>
                    </section>
                )
            }
            {/* =================================
                ALL CLAIMS
            ================================== */}
            <section className="claims-card">
                <div className="section-heading">
                    <div>
                        <p className="eyebrow">Backend facts</p>
                        <h2>Claims</h2>
                    </div>
                    <span>
                        {result.claims.length}{" "}
                        claims
                    </span>
                </div>
                <div className="claims-grid">
                    {
                        result.claims.map(
                            (claim) => (
                                <article
                                    key={claim.claim_id}
                                    className="claim-card"
                                >
                                    <div className="claim-header">
                                        <strong>
                                            {claim.claim_id}
                                        </strong>
                                        <span>
                                            {claim.fund_id}
                                        </span>
                                    </div>
                                    <p>
                                        {claim.text}
                                    </p>

                                    <div className="claim-meta">
                                        <span>Metric</span>
                                        <strong>
                                            {formatMetricName(claim.metric)}
                                        </strong>
                                    </div>
                                    <div className="claim-meta">
                                        <span>Computed value</span>
                                        <strong>
                                            {formatMetricValue(claim.metric, claim.value)}
                                        </strong>
                                    </div>
                                </article>
                            )
                        )
                    }
                </div>
            </section>

            {/* =================================
                AUDIT VIEW
            ================================== */}
            <section className="audit-card">
                <div className="section-heading">
                    <div>
                        <p className="eyebrow">Traceability</p>
                        <h2>Audit View</h2>
                    </div>
                </div>
                <p className="audit-description">
                    Each memo statement is linked
                    back to deterministic claims
                    created by the backend.
                </p>
                <div className="audit-list">
                    {
                        result.audit.map(
                            (
                                auditItem,
                                index
                            ) => (
                                <article
                                    key={
                                        `${auditItem.section}-${index}`
                                    }
                                    className="audit-item"
                                >
                                    <div className="audit-section-header">
                                        <h3>
                                            {formatSectionName(auditItem.section)}
                                        </h3>
                                    </div>
                                    {/* Memo statement */}
                                    <div className="memo-claim">
                                        <span className="audit-label">Memo statement</span>
                                        <p>{auditItem.memo_text}</p>
                                    </div>


                                    {/* Claim ID tags */}
                                    <div className="claim-tags">
                                        {
                                            auditItem.claim_ids.map((claimId) => (
                                                <span
                                                    key={claimId}
                                                    className="claim-tag"
                                                >
                                                    {claimId}
                                                </span>

                                            ))
                                        }
                                    </div>

                                    {/* Supporting claims */}
                                    <div className="supporting-claims">
                                        <span className="audit-label">
                                            Supporting claims
                                        </span>
                                        {
                                            auditItem.claims.map(
                                                (claim) => (
                                                    <div
                                                        key={claim.claim_id}
                                                        className="audit-claim-card"
                                                    >
                                                        <div className="claim-header">
                                                            <div>
                                                                <strong>
                                                                    {claim.claim_id}
                                                                </strong>
                                                                <span className="fund-id">
                                                                    {claim.fund_id}
                                                                </span>
                                                            </div>
                                                            <span>
                                                                {formatMetricName(claim.metric)}
                                                            </span>
                                                        </div>
                                                        <p>
                                                            {claim.text}
                                                        </p>
                                                        <div className="claim-value">
                                                            Computed value:{" "}
                                                            <strong>
                                                                {formatMetricValue(claim.metric, claim.value)}
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
                </div>
            </section>
        </main>
    );
};


// =====================================
// RANKED FUND CARD
// =====================================
interface RankedFundCardProps {
    fund: RankedFund;
}


const RankedFundCard = ({ fund }: RankedFundCardProps) => {
    return (
        <article className="ranked-fund-card">
            {/* Header */}
            <div className="ranked-fund-header">
                <div className="rank-badge">
                    <span>Rank</span>
                    <strong>#{fund.rank}</strong>
                </div>
                <div className="fund-title">
                    <h3>{fund.fund_name}</h3>
                    <p>
                        {fund.fund_id}
                        {" · "}
                        {fund.strategy}
                    </p>
                </div>
                <div className="score-box">
                    <span>Overall Score</span>
                    <strong>
                        {fund.score.toFixed(1)}
                    </strong>
                </div>
            </div>
            {/* Metadata */}
            <div className="fund-meta-grid">
                {
                    fund.manager_name && (
                        <FundMeta
                            label="Manager"
                            value={fund.manager_name}
                        />
                    )
                }
                {
                    fund.benchmark_ticker && (
                        <FundMeta
                            label="Benchmark"
                            value={fund.benchmark_ticker}
                        />

                    )
                }
                {
                    fund.redemption_frequency && (
                        <FundMeta
                            label="Liquidity"
                            value={fund.redemption_frequency}
                        />

                    )
                }
                {
                    fund.aum !== undefined && (
                        <FundMeta
                            label="AUM"
                            value={formatCurrency(fund.aum)}
                        />

                    )
                }
            </div>
            {/* Performance */}
            <div className="metrics-grid">
                <Metric
                    label="Annualized Return"
                    value={formatPercent(fund.performance.fund_annualized_return)}
                />
                <Metric
                    label="Volatility"
                    value={formatPercent(fund.performance.fund_volatility)}
                />

                <Metric
                    label="Sharpe Ratio"
                    value={fund.performance.sharpe_ratio !== null
                        ? fund.performance
                            .sharpe_ratio
                            .toFixed(2)
                        : "N/A"
                    }
                />
                <Metric
                    label="Excess Return"
                    value={formatPercent(fund.performance.excess_return)}
                />
                <Metric
                    label="Max Drawdown"
                    value={formatPercent(fund.performance.fund_max_drawdown)}
                />
                <Metric
                    label="Correlation"
                    value={fund.performance.correlation.toFixed(2)}
                />
                <Metric
                    label="Observations"
                    value={String(fund.performance.observations)}
                />
                <Metric
                    label="Benchmark Return"
                    value={formatPercent(fund.performance.benchmark_annualized_return)}
                />

            </div>

            {/* Score breakdown */}
            <div className="score-breakdown">
                <h4>Score Breakdown</h4>
                <div className="score-breakdown-grid">
                    <Metric
                        label="Mandate"
                        value={String(fund.score_breakdown.mandate_score)}
                    />
                    <Metric
                        label="Sharpe"
                        value={String(fund.score_breakdown.sharpe_score)}
                    />
                    <Metric
                        label="Excess Return"
                        value={String(fund.score_breakdown.excess_return_score)}
                    />
                    <Metric
                        label="Drawdown"
                        value={String(fund.score_breakdown.drawdown_score)}
                    />
                </div>
            </div>

            {/* Rationale */}
            {
                fund.reasons.length > 0 && (
                    <div className="rationale">
                        <h4>
                            Ranking Rationale
                        </h4>
                        <ul>
                            {
                                fund.reasons.map((reason, index) => (
                                    <li key={`${fund.fund_id}-reason-${index}`}>
                                        {reason}
                                    </li>
                                )
                                )
                            }

                        </ul>
                    </div>
                )
            }
        </article>
    );
};


// =====================================
// MEMO SECTION
// =====================================


interface MemoSectionProps {
    title: string;
    text: string;
    claimIds: string[];
}


const MemoSection = ({
    title,
    text,
    claimIds,
}: MemoSectionProps) => {
    return (
        <div className="memo-section">
            <h3>{title}</h3>
            <p>{text}</p>
            <div className="claim-tags">
                {
                    claimIds.map((claimId) => (
                        <span key={claimId} className="claim-tag">
                            {claimId}
                        </span>
                    )
                    )
                }
            </div>
        </div>
    );
};


// =====================================
// METRIC
// =====================================


interface MetricProps {
    label: string;
    value: string;
}


const Metric = ({ label, value }: MetricProps) => {
    return (
        <div className="metric">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
    );
};


// =====================================
// FUND META
// =====================================


interface FundMetaProps {
    label: string;
    value: string;
}


const FundMeta = ({ label, value }: FundMetaProps) => {
    return (
        <div className="fund-meta">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
    );
};


// =====================================
// FORMATTERS
// =====================================


const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
};


const formatCurrency = (value: number) => {
    return new Intl.NumberFormat(
        "en-US",
        {
            style: "currency",
            currency: "USD",
            notation: "compact",
            maximumFractionDigits: 1,
        }
    ).format(value);
};


const formatMetricValue = (
    metric: string,
    value: unknown
) => {
    const percentMetrics = [
        "fund_annualized_return",
        "benchmark_annualized_return",
        "fund_volatility",
        "benchmark_volatility",
        "excess_return",
        "fund_max_drawdown",
        "benchmark_max_drawdown",
        "risk_free_rate",
    ];

    if (
        typeof value === "number" &&
        percentMetrics.includes(
            metric
        )
    ) {
        return formatPercent(
            value
        );
    }

    if (
        typeof value === "number" &&
        (
            metric === "sharpe_ratio" ||
            metric === "correlation"
        )
    ) {

        return value.toFixed(
            2
        );
    }


    if (
        metric === "aum" &&
        typeof value === "number"
    ) {
        return formatCurrency(
            value
        );
    }

    return String(
        value
    );
};


const formatMetricName = (metric: string) => {
    return metric
        .replaceAll(
            "_",
            " "
        )
        .replace(
            /\b\w/g,
            (
                letter
            ) =>
                letter.toUpperCase()
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
            (
                letter
            ) =>
                letter.toUpperCase()
        );
};


export default Result;
