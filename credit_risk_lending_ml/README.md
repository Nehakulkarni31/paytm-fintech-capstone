# Part 2: Credit Risk & Lending ML

## Execution Instructions

1. Run `python generate_data.py` to generate `credit_applicants.csv` and `txn_behaviour.csv`.
2. Run `python model_pipeline.py` to execute the end-to-end preprocessing, classification, risk-pricing, and anomaly detection pipeline.

## Preprocessing & Thin-File Handling Justification

To serve "new-to-credit" applicants, rows with missing `credit_bureau_score` values were not dropped. Instead:

1. An `is_thin_file` binary flag was engineered directly from the raw data prior to any splitting or imputation.
2. The dataset was split 75/25 (stratified on the default label to maintain the 20.25% default rate).
3. The median `credit_bureau_score` was computed **strictly from the training split** and used to impute missing values in both the train and test sets. This prevents data leakage (where test-set statistics inappropriately influence the training phase) while allowing the model to leverage alternative data (like UPI inflow) for thin-file applicants.

## Bias-Awareness Note & Governance Recommendation

Even without explicit protected attributes like gender, race, or religion in this dataset, a correlated proxy risk exists. For example, `employment_type` (particularly the "gig" worker classification) or `monthly_income_inr` could inadvertently correlate with specific demographic groups, geographic areas, or socioeconomic backgrounds. If the model aggressively penalizes gig workers, it may inadvertently cause disparate impact against marginalized populations who rely heavily on the gig economy.

**Recommended Governance Step:**
Before this model goes live, I recommend implementing a **"maker-checker" human-in-the-loop review** specifically for declined thin-file applicants and those flagged in the highest risk tier (Tier 4). A human credit analyst should periodically audit a random sample of these automated declines to ensure the model isn't systematically denying credit based on proxy variables, ensuring fairer outcomes for non-traditional applicants.

## Final Model Recommendation

Based on the side-by-side evaluation, **I recommend deploying the Logistic Regression model** for Paytm Postpaid.

- **Performance:** Logistic Regression significantly outperformed the Decision Tree, achieving an ROC AUC of 0.7188 (compared to the Decision Tree's 0.5312) and a higher F1 Score (0.3684 vs 0.2667).
- **Calibration:** More importantly for risk-based pricing, Logistic Regression outputs well-calibrated probabilities. As demonstrated in the risk-tier table, binning the Logistic Regression probabilities resulted in a perfectly monotonically increasing observed default rate (8.0% -> 12.0% -> 20.0% -> 40.0%), which is essential for safely assigning tiered interest rates.
- **Fraud Sub-Task:** The Isolation Forest successfully flagged 73.3% (11 out of 15) of the injected anomalies, providing a strong supplementary layer of transaction security alongside the credit decisioning.
