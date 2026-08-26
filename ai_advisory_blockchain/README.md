# Part 3: AI-Augmented FinTech Advisory & Blockchain Risk

## Execution Instructions

1. Run `python advisory_agent.py` to execute the Think-Act-Observe portfolio advisory agent.
2. Run `python extract_disclosure.py` to run the structured JSON extraction on corporate disclosures.
3. Run `python debate.py` to view the multi-agent Bull/Bear/Synthesizer debate.
4. Run `python dcf_calculator.py` to view the Discounted Cash Flow baseline valuation and sensitivity grid.

## Environment & Design Details

- **LLM Mode:** All recorded outputs and transcripts were generated using the graded baseline mode (`MOCK_LLM=1` or left unset). No live API network calls were made, ensuring deterministic rule-based evaluation per the rubric constraints.
- **FCFF Growth Simplification:** In the DCF model, the 5-year projected FCFF utilizes a flat 15% growth rate rather than mathematically fading year-over-year toward the terminal rate. This was a deliberate modeling simplification to establish the base 5-year projection before the distinct terminal phase.

---

## Example Run Transcripts (MOCK_LLM=1)

### 1. Advisory Agent (`advisory_agent.py`)

```text
--- ADVISORY AGENT RUN SCRIPT ---

Processing INV01 (Conservative Risk Tolerance)...
  -> [THINK] Determining target allocation...
  -> [ACT] Calling get_stock_data tool for ['PAYBOND', 'PAYGOLD', 'PAYRETAIL']...
  -> [OBSERVE] Calculating CAPM return and portfolio variance...
  -> [DECISION] Finalized: For Conservative investor INV01, we recommend an allocation across ['PAYBOND', 'PAYGOLD', 'PAYRETAIL'] with an expected portfolio return of 9.20% and volatility of 8.44%.

Processing INV02 (Moderate Risk Tolerance)...
  -> [THINK] Determining target allocation...
  -> [ACT] Calling get_stock_data tool for ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD']...
  -> [OBSERVE] Calculating CAPM return and portfolio variance...
  -> [DECISION] Finalized: For Moderate investor INV02, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.30% and volatility of 12.57%.

Processing INV03 (Aggressive Risk Tolerance)...
  -> [THINK] Determining target allocation...
  -> [ACT] Calling get_stock_data tool for ['PAYTECH', 'PAYFIN', 'PAYINFRA']...
  -> [OBSERVE] Calculating CAPM return and portfolio variance...
  -> [DECISION] ESCALATED_TO_HUMAN_ADVISOR
     Reason: Portfolio volatility (20.58%) exceeds 20% safe threshold. (Expected Return: 15.00%)

Processing INV04 (Moderate Risk Tolerance)...
  -> [THINK] Determining target allocation...
  -> [ACT] Calling get_stock_data tool for ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD']...
  -> [OBSERVE] Calculating CAPM return and portfolio variance...
  -> [DECISION] Finalized: For Moderate investor INV04, we recommend an allocation across ['PAYRETAIL', 'PAYINFRA', 'PAYGOLD'] with an expected portfolio return of 11.30% and volatility of 12.57%.

Processing INV05 (Aggressive Risk Tolerance)...
  -> [THINK] Determining target allocation...
  -> [ACT] Calling get_stock_data tool for ['PAYTECH', 'PAYFIN', 'PAYINFRA']...
  -> [OBSERVE] Calculating CAPM return and portfolio variance...
  -> [DECISION] ESCALATED_TO_HUMAN_ADVISOR
     Reason: Portfolio volatility (20.58%) exceeds 20% safe threshold. (Expected Return: 15.00%)
```

### 2. Disclosure Extraction (`extract_disclosure.py`)

```text
--- DISCLOSURE EXTRACTION RUN SCRIPT ---

Analyzing: doc_01: Assuming input costs remain stable through the next ...
{
  "risk_flags": [],
  "hedging_detected": true,
  "sentiment": "cautious"
}

Analyzing: doc_02: The company faces an ongoing litigation matter relat...
{
  "risk_flags": [
    "Identified potential legal/regulatory/concentration risk."
  ],
  "hedging_detected": false,
  "sentiment": "neutral"
}

Analyzing: doc_03: Our top three customers together account for approxi...
{
  "risk_flags": [
    "Identified potential legal/regulatory/concentration risk."
  ],
  "hedging_detected": false,
  "sentiment": "neutral"
}

Analyzing: doc_04: We remain cautiously optimistic about demand recover...
{
  "risk_flags": [],
  "hedging_detected": true,
  "sentiment": "cautious"
}

Analyzing: doc_05: The board is confident in the long-term strategy and...
{
  "risk_flags": [],
  "hedging_detected": false,
  "sentiment": "confident"
}

Analyzing: doc_06: A recent regulatory notice has been received regardi...
{
  "risk_flags": [
    "Identified potential legal/regulatory/concentration risk."
  ],
  "hedging_detected": false,
  "sentiment": "neutral"
}
```

### 3. Multi-Agent Debate (`debate.py`)

```text
--- MULTI-AGENT DEBATE FOR PAYTECH ---

[BULL AGENT]: With an expected return of 19.0% against a beta of 1.55, PAYTECH offers highly attractive risk-adjusted upside for growth-oriented portfolios.

[BEAR AGENT]: While the upside is notable, PAYTECH's extreme standard deviation of 34.0% exposes investors to massive downside risk during market corrections.

[SYNTHESIZER]: The Bull correctly highlights PAYTECH's strong 19.0% expected return. However, the Bear's warning regarding its 34.0% volatility is valid. Recommendation: Limit PAYTECH to a small satellite position rather than a core holding.
```

### 4. DCF Valuation (`dcf_calculator.py`)

```text
--- PART D: DCF VALUATION CALCULATOR ---
Base Year FCFF (Unlevered): 275.0 INR Cr
Base Case WACC: 12.37%

DCF Sensitivity Table (Enterprise Value in INR Cr):
            TG 3.0%  TG 4.0%  TG 5.0%
WACC 11.4%   5488.0   6071.0   6837.0
WACC 12.4%   4868.0   5311.0   5873.0
WACC 13.4%   4369.0   4714.0   5141.0

EV/EBITDA Cross-Check Valuation: 5100.0 INR Cr

--- Written Comparison ---
The DCF valuation yields a baseline enterprise value of 5,311 INR Cr, which aligns closely (within ~4%) with the EV/EBITDA multiples approach valuation of 5,100 INR Cr. This convergence suggests that the near-term cash flow growth and conservative perpetual growth assumptions appropriately reflect the market-implied multiple, providing stronger confidence in the overall valuation.
```
