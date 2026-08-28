# Allocator Memo Builder (IC Draft + Audit Trail)

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


## STEPS

##### 1. Does the input CSV validate the mandate

**********************************************************
liquidity_pass = fund.redemption_frequency <= mandate.liquidity_requirement
volatility_pass = 8% <= fund.volatility <= 12%
drawdown_pass = abs(fund.max_drawdown) <= 15%
strategy_pass = fund.strategy in preferred_strategies



{
  "fund_id": "F001",
  "checks": {
    "liquidity": {"value": "Monthly", "pass": true},
    "volatility": {"value": 0.092, "pass": true},
    "max_drawdown": {"value": -0.114, "pass": true},
    "strategy": {"value": "Long/Short Equity", "pass": true}
  }
}
**********************************************************

#### 2. Normalize and validate the dataset (missing values, inconsistent date ranges, mismatched fund identifiers).

#### 3. Pull benchmark return data from a public market data API (e.g., Yahoo Finance, FRED, or similar) so fund performance can be compared against relevant indices.

**********************************************************
Fund annualized return vs. SPY
Fund volatility vs. SPY
Fund max drawdown vs. SPY
Fund/benchmark correlation
Excess return
**********************************************************


### 4. Compute allocator-grade summary metrics (e.g., drawdown, vol, Sharpe, correlation to a benchmark or to peers).

{
  "fund_id": "F001",
  "benchmark_ticker": "SPY",

  "fund_metrics": {
    "annualized_return": 0.0607,
    "annualized_volatility": 0.0648,
    "sharpe_ratio": 0.94,
    "max_drawdown": -0.0200
  },

  "benchmark_metrics": {
    "annualized_return": 0.164,
    "annualized_volatility": 0.105,
    "sharpe_ratio": 1.56,
    "max_drawdown": -0.031
  },

  "comparison": {
    "excess_return": -0.1033,
    "correlation": 0.82
  }
}

5. Use an LLM to produce a ranked shortlist with rationale and a 1-2 page IC-style memo (summary, recommendation, key risks, and a data appendix).

6. Provide an audit view where memo claims link back to either a computed metric or a specific source field.




logging is left out of the project because of the demo
