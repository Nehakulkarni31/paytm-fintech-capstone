import sqlite3
import pandas as pd

def build_database_and_query():

    conn = sqlite3.connect('paytm_payments.db')
    cursor = conn.cursor()

    cursor.executescript('''
    DROP TABLE IF EXISTS transactions;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS merchants;

    CREATE TABLE merchants(
        merchant_id INTEGER PRIMARY KEY,
        merchant_name TEXT,
        category TEXT,
        region TEXT
    );

    CREATE TABLE users(
        user_id INTEGER PRIMARY KEY,
        signup_date TIMESTAMP
        );

    CREATE TABLE transactions(
        transaction_id TEXT PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        merchant_id INTEGER REFERENCES merchants(merchant_id),
        transaction_time TIMESTAMP,
        amount_inr INTEGER,
        payment_method TEXT,
        status TEXT,
        risk_score INTEGER
    );
    ''')

    pd.read_csv('merchants.csv').to_sql('merchants', conn, if_exists='append', index=False)
    pd.read_csv('users.csv').to_sql('users', conn, if_exists='append', index=False)
    pd.read_csv('ledger.csv').to_sql('transactions', conn, if_exists='append', index=False)

    print("Database built and data loaded successfully.\n" + "-"*50)

    queries = {
        "1. Quantify Chargeback Impact (SELECT, WHERE, DISTINCT)": """
            SELECT 
                COUNT(DISTINCT transaction_id) AS total_chargebacks,
                COUNT(DISTINCT user_id) AS unique_users_affected,
                SUM(amount_inr) AS total_chargeback_value
            FROM transactions
            WHERE status = 'chargeback';
        """,

        "2. Identify Burner Accounts (INNER JOIN, exact 30 day boundary logic)": """
            SELECT t.transaction_id, t.user_id, t.transaction_time, t.amount_inr,
            CAST((julianday(t.transaction_time)-julianday(u.signup_date)) AS INTEGER) AS account_age_days
            FROM transactions t
            INNER JOIN users u ON t.user_id = u.user_id
            WHERE t.status = 'chargeback'
                AND (julianday(t.transaction_time)-julianday(u.signup_date)) >= 0
                AND (julianday(t.transaction_time) - julianday(u.signup_date)) < 30;
        """,

        "3. Detect Velocity Attacks (GROUP BY, HAVING, ORDER BY, 10-min bucket hack)": """
            SELECT
                user_id,
                substr(transaction_time, 1, 15) || '0:00' AS ten_min_window,
                COUNT(transaction_id) AS txn_count,
                SUM(amount_inr) AS total_amount
            FROM transactions
            GROUP BY user_id, ten_min_window
            HAVING txn_count>=3
            ORDER BY txn_count DESC;
        """,

        "4. Merchants with Zero (LEFT JOIN)": """
        SELECT
            m.merchant_name,
            COUNT(t.transaction_id) AS chargeback_count
        FROM merchants m
        LEFT JOIN transactions t ON m.merchant_id = t.merchant_id AND t.status = 'chargeback'
        GROUP BY m.merchant_name
        HAVING chargeback_count = 0
        LIMIT 5;
        """,

        "5. Top 5 Categories by Average Amount (LIMIT)":"""
        SELECT
            m.category,
            ROUND(AVG(t.amount_inr), 2) AS avg_txn_value
        FROM transactions t
        INNER JOIN merchants m ON t.merchant_id = m.merchant_id
        GROUP BY m.category
        ORDER BY avg_txn_value DESC
        LIMIT 5;

        """,

        "6. Overall Success Rate by Region": """
            SELECT 
                m.region, 
                COUNT(t.transaction_id) AS total_txns,
                ROUND(SUM(CASE WHEN t.status='captured' THEN 1 ELSE 0 END) * 100.0 / COUNT(t.transaction_id), 2) AS success_rate_percent
            FROM transactions t
            INNER JOIN merchants m ON t.merchant_id = m.merchant_id
            GROUP BY m.region
            ORDER BY total_txns DESC;
        """

    }

    for title, sql in queries.items():
        print(f"\n{title}\nSQL Query:")
        print(sql.strip())
        print("\nResults:")
        result_df = pd.read_sql_query(sql, conn)
        print(result_df. to_string(index=False))
        print("\n"+"="*60)

    conn.close()

if __name__ == "__main__":
    build_database_and_query() 
