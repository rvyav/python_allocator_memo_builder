# APPLICATION NAME: Allocator Memo Builder (IC Draft + Audit Trail)

## REQUIREMENTS

Integration: Market Data API (e.g., Yahoo Finance, FRED)

Build a web application that helps an allocator go from a small, messy "fund universe" dataset to a defendable investment committee memo.
 
Input: a CSV (or a few CSVs) representing a fund universe (fund name, strategy, liquidity terms, fee terms, monthly returns or summary stats, and a few qualitative notes) plus a simple "mandate" form with constraints (liquidity requirement, target volatility, max drawdown tolerance, strategy preferences/exclusions).

The system should:
Normalize and validate the dataset (missing values, inconsistent date ranges, mismatched fund identifiers).
Pull benchmark return data from a public market data API (e.g., Yahoo Finance, FRED, or similar) so fund performance can be compared against relevant indices.
Compute allocator-grade summary metrics (e.g., drawdown, vol, Sharpe, correlation to a benchmark or to peers).
Use an LLM to produce a ranked shortlist with rationale and a 1-2 page IC-style memo (summary, recommendation, key risks, and a data appendix).
Provide an audit view where memo claims link back to either a computed metric or a specific source field.
 
Think: "I upload a scrappy manager universe CSV, select constraints, the system pulls live benchmark data for comparison, and I get a memo draft that I can verify claim-by-claim."


