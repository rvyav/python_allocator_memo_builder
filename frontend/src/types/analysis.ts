export interface Claim {
    claim_id: string;
    fund_id: string;
    text: string;
    metric: string;
    value: number;
}

export interface Performance {
    fund_annualized_return: number;
    benchmark_annualized_return: number;
    fund_volatility: number;
    benchmark_volatility: number;
    fund_max_drawdown: number;
    benchmark_max_drawdown: number;
    correlation: number;
    excess_return: number;
    sharpe_ratio: number;
    risk_free_rate: number;
    observations: number;
}

export interface ScoreBreakdown {
    mandate_score: number;
    sharpe_score: number;
    excess_return_score: number;
    drawdown_score: number;
    overall_score: number;
}

export interface RankedFund {
    fund_id: string;
    fund_name: string;
    strategy: string;
    score: number;
    score_breakdown: ScoreBreakdown;
    performance: Performance;
    reasons: string[];
    rank: number;
}

export interface MemoSection {
    text: string;
    claim_ids: string[];
}

export interface DataAppendixItem {
    label: string;
    value: string;
    claim_ids: string[];
}

export interface Memo {
    summary: MemoSection;
    recommendation: MemoSection;
    key_risks: MemoSection;
    data_appendix: DataAppendixItem[];
}

export interface AuditItem {
    section: string;
    memo_text: string;
    claim_ids: string[];
    claims: Claim[];
}

export interface AnalysisData {
    filename: string;
    row_count: number;
    rows: unknown[];
    ranked_shortlist: RankedFund[];
    claims: Claim[];
    memo: Memo;
    audit: AuditItem[];
}

export interface UploadResponse {
    message: string;

    data: AnalysisData;
}
