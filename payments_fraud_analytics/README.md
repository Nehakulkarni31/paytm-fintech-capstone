# Part 1: Payments & Fraud Analytics

## Setup and Execution

1. Ensure `pandas`, `matplotlib`, and `seaborn` are installed.
2. Run `python generate_data.py` to generate the raw CSVs.
3. The spreadsheet logic is saved in `merchant_workbook.xlsx`.
4. Run `python sql_analysis.py` to build the SQLite database (`paytm_payments.db`) and output the 6 required queries (including burner account and velocity attack detection).
5. Run `python reconcile.py` to execute the payment reconciliation engine via Pandas.
6. Run `python dashboard.py` to generate the 4 required dashboard `.png` layers.

## Spreadsheet Design Decisions (merchant_workbook.xlsx)

- **HLOOKUP Fee Tiers:** I assumed a standard MDR fee structure for the HLOOKUP demonstration (UPI: 0.00%, Wallet: 1.50%, Card: 2.00%, Netbanking: 1.00%).
- **Nested IF/AND Classification:** The "High-Value Merchant Day" flag uses the exact logic: `(Daily Transaction Total > 5000 INR) AND (Region != 'East')`. The daily total was calculated inline using `SUMIFS` and validated using a dedicated 'Daily Pivot' sheet.

## Dashboard Interpretations

**1. Headline Layer:**
The platform maintains a strong overall success rate above 85%, though the reconciliation match rate indicates operational friction with the gateway. A platform-wide chargeback ratio of ~5.1% warrants immediate fraud-prevention tuning.

**2. Trends Layer:**
GMV remains relatively stable day-over-day, but distinct spikes in chargeback counts occur periodically. This suggests coordinated fraud attacks (like the injected burner accounts) targeting specific time windows rather than ambient daily fraud.

**3. Breakdown Layer:**
Card and UPI dominate the payment mix, representing the vast majority of successful GMV. Merchant categories like Ecommerce and Entertainment drive the highest volume, making them prime candidates for tighter risk controls.

**4. Details Layer:**
Among our highest-volume merchants, several exhibit a chargeback ratio well above the 1% acceptable threshold (highlighted in red in the table). These specific merchants require immediate manual review or temporary payout holds to mitigate ongoing risk.
