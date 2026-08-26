# Part 2: Credit Risk & Lending ML

## Execution Instructions

1. Run `python generate_data.py` to generate `credit_applicants.csv` and `txn_behaviour.csv`.
2. Run `python model_pipeline.py` to execute the end-to-end preprocessing, classification, risk-pricing, and anomaly detection pipeline.

## Preprocessing & Thin-File Handling Justification

To serve "new-to-credit" applicants, rows with missing `credit_bureau_score` values were not dropped. Instead:

1. An `is_thin_file` binary flag was engineered directly from the raw data prior to any splitting or imputation.
2. The dataset was split 75/25 (stratified on the default label to maintain the 20.25% default rate).
3. The median `credit_bureau_score` was computed **strictly from the training split** and used to impute missing values in both the train and test sets. This prevents data leakage while allowing the model to leverage alternative data (like UPI inflow) for thin-file applicants.

## Bias-Awareness Note & Governance Recommendation

Even without explicit protected attributes like gender, race, religion, or location in this dataset, significant correlated proxy risks exist in a real-world deployment. For example, `employment_type` (particularly the "gig" worker classification) or `monthly_income_inr` could inadvertently correlate with specific demographic groups or socioeconomic backgrounds.

Furthermore, relying heavily on `credit_bureau_score`—or the absence of one (thin-file status)—can perpetuate historical inequities. In India, geography, historical lending discrimination, and socioeconomic mobility are often deeply intertwined with caste and religion. Consequently, an algorithm that heavily penalizes lower incomes or a lack of formal credit history may inadvertently redline marginalized communities, leading to systemic disparate impact even if the model is mathematically "blind" to demographic labels.

**Recommended Governance Steps:**
Before this model goes live, I recommend two critical governance protocols:

1. **Maker-Checker Human-in-the-Loop Review:** specifically for declined thin-file applicants and those flagged in the highest risk tier (Tier 4). A human credit analyst should periodically audit a random sample of these automated declines to ensure the model isn't systematically denying credit based on proxy variables.
2. **Routine Disparate-Impact Audits:** By periodically and securely matching a sample of model predictions against demographic data in a siloed environment, the risk team can statistically measure and correct for unintentional bias across protected segments before the model scales.

## Final Model Comparison & Recommendation

| Metric                      | Logistic Regression | Decision Tree |
| :-------------------------- | :------------------ | :------------ |
| **Accuracy**                | 0.7600              | 0.6700        |
| **Precision**               | 0.3889              | 0.2400        |
| **Recall**                  | 0.3500              | 0.3000        |
| **F1 Score**                | 0.3684              | 0.2667        |
| **ROC AUC**                 | 0.7188              | 0.5312        |
| **Isolation Forest Recall** | 73.3% (11/15)       | N/A           |

Based on the side-by-side evaluation table above, **I recommend deploying the Logistic Regression model** for Paytm Postpaid.

- **Performance:** Logistic Regression significantly outperformed the Decision Tree, achieving an ROC AUC of 0.7188 (compared to the Decision Tree's 0.5312) and a higher F1 Score.
- **Calibration for Risk-Based Pricing:** More importantly, Logistic Regression outputs well-calibrated probabilities. Binning the Logistic Regression probabilities resulted in a perfectly monotonically increasing observed default rate (8.0% -> 12.0% -> 20.0% -> 40.0%), which is essential for safely assigning tiered interest rates.
- **Fraud Sub-Task:** The Isolation Forest successfully flagged 73.3% of the injected anomalies, providing a strong supplementary layer of transaction security alongside the credit decisioning.
