# Part 3: AI-Augmented FinTech Advisory & Blockchain Risk

## Execution Instructions

1. Run `python advisory_agent.py` to execute the Think-Act-Observe portfolio advisory agent.
2. Run `python extract_disclosure.py` to run the structured JSON extraction on corporate disclosures.
3. Run `python debate.py` to view the multi-agent Bull/Bear/Synthesizer debate.
4. Run `python dcf_calculator.py` to view the Discounted Cash Flow baseline valuation and sensitivity grid.

## Environment Details

- **LLM Mode:** All recorded outputs and transcripts were generated using the graded baseline mode (`MOCK_LLM=1` or left unset). No live API network calls were made, ensuring deterministic rule-based evaluation per the rubric constraints.

## Example Output: DCF Sensitivity Table

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
```
