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
