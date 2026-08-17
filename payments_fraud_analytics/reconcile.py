import pandas as pd

def reconcile_payments(ledger_df, gateway_df):
    """
    Compares the internal ledger against the gateway export to find discrepancies.
    Returns 4 DataFrames: missing_in_gateway, missing_in_ledger, amount_mismatches, status_mismatches,
    """

    ledger_ids = set(ledger_df['transaction_id'])
    gateway_ids = set(gateway_df['transaction_id'])

    missing_in_gateway = ledger_df[ledger_df['transaction_id'].isin(ledger_ids -  gateway_ids)]
    extra_in_gateway = gateway_df[gateway_df['transaction_id'].isin(gateway_ids - ledger_ids)]

    merged_df = pd.merge(
        ledger_df,
        gateway_df,
        on='transaction_id',
        suffixes=('_ledger','_gateway'),
        how='inner'
    )

    amount_mask = merged_df['amount_inr_ledger']!= merged_df['amount_inr_gateway']
    amount_mismatches = merged_df[amount_mask].copy()
    amount_mismatches['difference'] = amount_mismatches['amount_inr_ledger'] - amount_mismatches['amount_inr_gateway']
    
    # Status Mismatches
    status_mask = merged_df['status_ledger'] != merged_df['status_gateway']
    status_mismatches = merged_df[status_mask]
    return missing_in_gateway, extra_in_gateway, amount_mismatches, status_mismatches

if __name__ == "__main__":
    # Load the specific CSVs
    ledger = pd.read_csv('ledger.csv')
    gateway = pd.read_csv('gateway_export.csv')
    
    # Run the reconciliation
    missing, extra, amt_mismatch, stat_mismatch = reconcile_payments(ledger, gateway)
    
    # Print the findings
    total_ledger = len(ledger)
    print("--- RECONCILIATION SUMMARY ---")
    print(f"Total Transactions in Ledger: {total_ledger}\n")
    
    print(f"1. Missing in Gateway: {len(missing)} transactions (~{(len(missing)/total_ledger)*100:.1f}% rate)")
    print(f"2. Extra in Gateway: {len(extra)} transactions (~{(len(extra)/total_ledger)*100:.1f}% rate)")
    print(f"3. Amount Mismatches: {len(amt_mismatch)} transactions (~{(len(amt_mismatch)/total_ledger)*100:.1f}% rate)")
    print(f"4. Status Mismatches: {len(stat_mismatch)} transactions (~{(len(stat_mismatch)/total_ledger)*100:.1f}% rate)")
    print("\nReconciliation engine executed successfully.")