# Paytm FinTech Analytics & AI Platform - Capstone Project

This repository contains the comprehensive capstone project for the Executive Certification in FinTech & Artificial Intelligence. It simulates a cohesive analytics and machine learning platform for Paytm, spanning three distinct verticals: Payments, Lending, and Wealth Advisory.

## Project Structure

- `/payments_fraud_analytics` (Part 1): Operations, SQL databases, spreadsheet logic, and dashboarding.
- `/credit_risk_lending_ml` (Part 2): End-to-end ML classification pipeline, risk-based pricing, and anomaly detection.
- `/ai_advisory_blockchain` (Part 3): Agentic (Think-Act-Observe) advisory loops, NLP extraction, DCF valuation, and blockchain risk analysis.

## Setup Instructions

This project uses a consolidated `requirements.txt` at the repository root. To set up the environment, run:

```bash
pip install -r requirements.txt
```

## How to Run Each Part

### Part 1 — Payments & Fraud Analytics

```bash
cd payments_fraud_analytics
python generate_data.py      # generates merchants.csv, users.csv, ledger.csv, gateway_export.csv
python sql_analysis.py       # builds paytm_payments.db and runs the 6 required SQL queries
python reconcile.py          # runs reconcile_payments() against ledger vs. gateway export
python dashboard.py          # generates the 4 dashboard layer PNGs
```

The Excel workbook (`merchant_workbook.xlsx`) is a static committed artifact — open it directly in Excel/Sheets/LibreOffice.

### Part 2 — Credit Risk & Lending ML

```bash
cd credit_risk_lending_ml
python generate_data.py      # generates credit_applicants.csv, txn_behaviour.csv
python model_pipeline.py     # runs preprocessing, both classifiers, risk-pricing table, anomaly detection
```

### Part 3 — AI Advisory & Blockchain Risk

```bash
cd ai_advisory_blockchain
python advisory_agent.py     # Think-Act-Observe portfolio agent for all 5 investor profiles
python extract_disclosure.py # structured JSON extraction on all 6 disclosure snippets
python debate.py             # bull/bear/synthesizer debate demo
python dcf_calculator.py     # DCF valuation + 3x3 sensitivity table + EV/EBITDA cross-check
```

All scripts default to `MOCK_LLM=1` (deterministic, no API key or network call required).

## Design Decisions Summary

**Part 1:** MDR fee tiers for the HLOOKUP demo were assumed (UPI 0%, Wallet 1.5%, Card 2%, Netbanking 1%). The "High-Value Merchant Day" rule is `(daily merchant total > INR 5,000) AND (region != "East")`, computed inline via `SUMIFS` and cross-validated against a dedicated Daily Pivot sheet.

**Part 2:** Thin-file applicants are never dropped — an `is_thin_file` flag is engineered pre-split, then `credit_bureau_score` is median-imputed using training-split statistics only, applied to both splits, to avoid leakage. Isolation Forest contamination was set to match the seeded anomaly rate (15/265 ≈ 5.7%).

**Part 3:** The advisory agent's allocations, CAPM returns, and portfolio volatility follow the prescribed lookup table and formulas exactly, using only `beta` (never `analyst_expected_return`) for CAPM. The DCF's terminal growth rate (4%) was chosen ≥3 points below base-case WACC (12.37%) so WACC exceeds terminal growth in all 9 sensitivity grid cells.

## Academic Integrity

All code, analysis, and written interpretations in this repository are original work, produced specifically for this capstone.
