import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import IsolationForest
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix)
import warnings
warnings.filterwarnings('ignore')

def run_part_a_preprocessing():
    print("--- PART A: EDA & PREPROCESSING ---")
    df = pd.read_csv("credit_applicants.csv")
    
    default_rate = df['default'].mean() * 100
    missing_pct = df['credit_bureau_score'].isna().mean() * 100
    print(f"Measured Default Rate: {default_rate:.2f}%")
    print(f"Missing credit_bureau_score: {missing_pct:.2f}% (Exactly 80 thin-file applicants)")
    
    # Engineer 'is_thin_file' flag BEFORE imputation/split
    df['is_thin_file'] = df['credit_bureau_score'].isna().astype(int)
    
    X = df.drop(columns=['applicant_id', 'default']) 
    y = df['default']
    
    # Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    
    # Median Imputation (Computed from Training Split ONLY)
    train_median_score = X_train['credit_bureau_score'].median()
    X_train['credit_bureau_score'] = X_train['credit_bureau_score'].fillna(train_median_score)
    X_test['credit_bureau_score'] = X_test['credit_bureau_score'].fillna(train_median_score)
    
    # Encode 'employment_type' 
    X_train = pd.get_dummies(X_train, columns=['employment_type'], drop_first=False)
    X_test = pd.get_dummies(X_test, columns=['employment_type'], drop_first=False)
    X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)
    
    # Scale numeric features (Fit on Train ONLY)
    numeric_cols = ['age', 'monthly_income_inr', 'existing_loans_count', 
                    'credit_utilization_ratio', 'upi_monthly_inflow_inr', 
                    'bounced_payments_count', 'credit_bureau_score']
    
    scaler = StandardScaler()
    X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    return X_train, X_test, y_train, y_test

def run_part_b_modeling(X_train, X_test, y_train, y_test):
    print("\n--- PART B: CLASSIFICATION & RISK-BASED PRICING ---")
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    
    # 1. Train Models
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_train, y_train)
    
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train, y_train)
    
    # 2. Predictions & Probabilities
    lr_preds, lr_probs = lr.predict(X_test), lr.predict_proba(X_test)[:, 1]
    dt_preds, dt_probs = dt.predict(X_test), dt.predict_proba(X_test)[:, 1]
    
    # 3. Evaluation Metrics Side-by-Side
    def get_metrics(y_true, y_pred, y_prob):
        return {
            "Accuracy": accuracy_score(y_true, y_pred),
            "Precision": precision_score(y_true, y_pred, zero_division=0),
            "Recall": recall_score(y_true, y_pred, zero_division=0),
            "F1 Score": f1_score(y_true, y_pred, zero_division=0),
            "ROC AUC": roc_auc_score(y_true, y_prob)
        }
        
    comp_df = pd.DataFrame({
        'Logistic Regression': get_metrics(y_test, lr_preds, lr_probs),
        'Decision Tree': get_metrics(y_test, dt_preds, dt_probs)
    })
    
    print("1. Model Comparison Table:")
    print(comp_df.round(4).to_string())
    print("\n2. Confusion Matrices:")
    print(f"Logistic Regression:\n{confusion_matrix(y_test, lr_preds)}")
    print(f"Decision Tree:\n{confusion_matrix(y_test, dt_preds)}")
    
    # NEW: Plot and save the ROC Curve visual
    fpr_lr, tpr_lr, _ = roc_curve(y_test, lr_probs)
    fpr_dt, tpr_dt, _ = roc_curve(y_test, dt_probs)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr_lr, tpr_lr, label=f'Logistic Regression (AUC = {comp_df.loc["ROC AUC", "Logistic Regression"]:.4f})')
    plt.plot(fpr_dt, tpr_dt, label=f'Decision Tree (AUC = {comp_df.loc["ROC AUC", "Decision Tree"]:.4f})')
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve Comparison')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('roc_curve.png', dpi=300)
    plt.close()
    print("\n[✔] Saved 'roc_curve.png' to directory.")
    
    # 4. Risk-Based Pricing Table
    print("\n3. Risk-Based Pricing Table:")
    pricing_df = pd.DataFrame({'actual_default': y_test, 'pred_prob': lr_probs})
    
    pricing_df['Risk_Tier'] = pd.qcut(pricing_df['pred_prob'], q=4, 
                                      labels=['Tier 1 (Lowest Risk)', 'Tier 2 (Medium-Low)', 
                                              'Tier 3 (Medium-High)', 'Tier 4 (Highest Risk)'])
    
    tier_stats = pricing_df.groupby('Risk_Tier').agg(
        Applicant_Count=('actual_default', 'count'),
        Observed_Default_Rate=('actual_default', lambda x: x.mean() * 100)
    ).reset_index()
    
    tier_stats['Assigned_Interest_Rate'] = ["10.0% - 12.9%", "13.0% - 15.9%", "16.0% - 19.9%", "20.0%+ (or Decline)"]
    tier_stats['Observed_Default_Rate'] = tier_stats['Observed_Default_Rate'].round(1).astype(str) + '%'
    
    print(tier_stats.to_string(index=False))

def run_part_c_anomaly_detection():
    print("\n--- PART C: ANOMALY DETECTION (Isolation Forest) ---")
    txn = pd.read_csv("txn_behaviour.csv")
    
    # Select numeric behavioural features and standardize
    features = ['txn_hour', 'is_new_device', 'txn_amount_inr']
    scaler = StandardScaler()
    X_txn_scaled = scaler.fit_transform(txn[features])
    
    # Run Isolation Forest matching injected anomaly proportion (15/265)
    contamination_rate = 15 / 265
    iso = IsolationForest(random_state=42, contamination=contamination_rate)
    txn['anomaly_pred'] = iso.fit_predict(X_txn_scaled)
    
    # Evaluate recall against injected ground truth (IDs starting with BTXNA)
    txn['is_true_anomaly'] = txn['txn_id'].str.startswith('BTXNA')
    caught = txn[(txn['is_true_anomaly'] == True) & (txn['anomaly_pred'] == -1)]
    
    print(f"Total transactions evaluated: {len(txn)}")
    print(f"Total seeded anomalies (ground truth): {txn['is_true_anomaly'].sum()}")
    print(f"Anomalies successfully flagged by model: {len(caught)}")
    print(f"Recall against ground truth: {(len(caught) / 15) * 100:.1f}%")

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = run_part_a_preprocessing()
    run_part_b_modeling(X_train, X_test, y_train, y_test)
    run_part_c_anomaly_detection()