

export const liquidityOptions = [
    "Daily",
    "Weekly",
    "Monthly",
    "Quarterly",
    "Semi-Annual",
    "Annual",
    "No preference",
];

export const volatilityOptions = [
    { value: "LOW", label: "Low (0–5%)" },
    { value: "LOW_MODERATE", label: "Low-Moderate (5–8%)" },
    { value: "MODERATE", label: "Moderate (8–12%)" },
    { value: "MODERATE_HIGH", label: "Moderate-High (12–16%)" },
    { value: "HIGH", label: "High (16%+)" },
    { value: "NO_TARGET", label: "No target" },
];

export const drawdownOptions = [
    { value: "CONSERVATIVE", label: "Conservative (≤5%)" },
    { value: "MODERATE", label: "Moderate (5–10%)" },
    { value: "ELEVATED", label: "Elevated (10–15%)" },
    { value: "AGGRESSIVE", label: "Aggressive (15–25%)" },
    { value: "NO_LIMIT", label: "No limit" },
];

export const strategyOptions = [
    "Global Macro",
    "Long/Short Equity",
    "Market Neutral",
    "Equity Long Bias",
    "Managed Futures",
    "Direct Lending",
    "Distressed Debt",
    "Structured Credit",
    "Fixed Income Relative Value",
    "Event Driven",
    "Special Situations",
    "Convertible Arbitrage",
    "Relative Value Volatility",
    "Quantitative Equity",
    "Risk Parity",
    "Real Assets",
    "Multi-Strategy",
];
