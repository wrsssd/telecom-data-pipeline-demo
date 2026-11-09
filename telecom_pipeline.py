import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd


DB_NAME = "telecom_data.db"
OUTPUT_CSV = "telecom_analytical_report.csv"


def init_db(conn):
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS tariffs;
        DROP TABLE IF EXISTS traffic_logs;

        CREATE TABLE tariffs (
            tariff_id INTEGER PRIMARY KEY,
            tariff_name TEXT,
            monthly_fee REAL
        );

        CREATE TABLE traffic_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            tariff_id INTEGER,
            event_date TEXT,
            mobile_mb REAL,
            fixed_mb REAL
        );
    """)

    tariffs = [
        (1, "Базовый", 450.0),
        (2, "Смарт Плюс", 750.0),
        (3, "Ультра Безлимит", 1200.0)
    ]
    cursor.executemany("INSERT INTO tariffs VALUES (?, ?, ?)", tariffs)

    logs = []
    base_date = datetime.now()
    
    for uid in range(101, 115):
        t_id = random.choice([1, 2, 3])
        for day in range(7):
            dt = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
            mob = round(random.uniform(150.0, 2800.0), 2)
            fix = round(random.uniform(600.0, 9500.0), 2)
            logs.append((uid, t_id, dt, mob, fix))

    cursor.executemany("""
        INSERT INTO traffic_logs (user_id, tariff_id, event_date, mobile_mb, fixed_mb)
        VALUES (?, ?, ?, ?, ?)
    """, logs)
    conn.commit()


def build_report(conn):
    query = """
    WITH user_totals AS (
        SELECT 
            t.user_id,
            tr.tariff_name,
            tr.monthly_fee,
            ROUND(SUM(t.mobile_mb) / 1024.0, 2) AS total_mobile_gb,
            ROUND(SUM(t.fixed_mb) / 1024.0, 2) AS total_fixed_gb,
            ROUND(SUM(t.mobile_mb + t.fixed_mb) / 1024.0, 2) AS total_traffic_gb
        FROM traffic_logs t
        JOIN tariffs tr ON t.tariff_id = tr.tariff_id
        GROUP BY t.user_id, tr.tariff_name, tr.monthly_fee
    )
    SELECT 
        user_id,
        tariff_name,
        monthly_fee,
        total_mobile_gb,
        total_fixed_gb,
        total_traffic_gb,
        RANK() OVER (PARTITION BY tariff_name ORDER BY total_traffic_gb DESC) AS rank_in_tariff
    FROM user_totals
    ORDER BY tariff_name, rank_in_tariff;
    """
    return pd.read_sql_query(query, conn)


if __name__ == "__main__":
    with sqlite3.connect(DB_NAME) as conn:
        init_db(conn)
        df_report = build_report(conn)
        
    df_report.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved report to {OUTPUT_CSV} ({len(df_report)} rows)")
    print(df_report.head(10))
