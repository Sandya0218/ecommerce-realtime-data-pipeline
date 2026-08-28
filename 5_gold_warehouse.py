"""
Step 5: Data Warehouse / Database (Gold Layer)
==============================================
Purpose:
  - Reads cleaned data from the Silver layer (data/silver/silver_orders.csv).
  - Loads the transactional records into a Gold layer SQLite database (data/gold/sales_warehouse.db)
    under the fact table `fact_sales_orders`.
  - Creates a business-ready aggregated summary table `agg_category_sales`.
"""

import os
import sqlite3
import pandas as pd

# File paths
SILVER_FILE_PATH = os.path.join("data", "silver", "silver_orders.csv")
GOLD_DIR_PATH = os.path.join("data", "gold")
GOLD_DB_PATH = os.path.join(GOLD_DIR_PATH, "sales_warehouse.db")


def build_gold_warehouse():
    """Reads Silver data and populates fact and summary tables in the Gold SQLite warehouse."""
    
    # 1. Check if Silver data exists
    if not os.path.exists(SILVER_FILE_PATH):
        print(f"[Error] Silver file not found at '{SILVER_FILE_PATH}'.")
        print("Please run Step 4 (Silver ETL) first.")
        return

    print("=" * 60)
    print("Building Gold Layer Data Warehouse")
    print("=" * 60)

    # 2. Read Silver CSV
    print(f"Reading cleaned data from: {SILVER_FILE_PATH}")
    df = pd.read_csv(SILVER_FILE_PATH)
    print(f"Loaded {len(df)} records from Silver layer.")

    # 3. Ensure Gold folder exists
    os.makedirs(GOLD_DIR_PATH, exist_ok=True)

    # 4. Connect to SQLite Gold Database
    print(f"Connecting to Gold database: {GOLD_DB_PATH}")
    conn = sqlite3.connect(GOLD_DB_PATH)

    # 5. Load fact table: fact_sales_orders
    table_fact = "fact_sales_orders"
    df.to_sql(table_fact, conn, if_exists="replace", index=False)
    print(f"Loaded table '{table_fact}' with {len(df)} rows.")

    # 6. Create Aggregated Summary: Category Sales Metrics
    agg_category = df.groupby("category").agg(
        total_orders=("order_id", "count"),
        total_units_sold=("quantity", "sum"),
        total_revenue=("total_amount", "sum"),
        avg_order_value=("total_amount", "mean")
    ).reset_index()
    
    agg_category["avg_order_value"] = agg_category["avg_order_value"].round(2)

    # 7. Load summary table: agg_category_sales
    table_summary = "agg_category_sales"
    agg_category.to_sql(table_summary, conn, if_exists="replace", index=False)
    print(f"Created summary table '{table_summary}' with {len(agg_category)} category metrics.")

    # 8. Query & Preview tables from SQLite database
    print("\n--- Preview: fact_sales_orders (first 3 rows) ---")
    preview_fact = pd.read_sql_query(f"SELECT * FROM {table_fact} LIMIT 3", conn)
    print(preview_fact)

    print("\n--- Preview: agg_category_sales (Full Summary) ---")
    preview_summary = pd.read_sql_query(f"SELECT * FROM {table_summary}", conn)
    print(preview_summary)

    # Close connection
    conn.close()
    print(f"\n[SUCCESS] Step 5 Gold Data Warehouse created at '{GOLD_DB_PATH}'!")


if __name__ == "__main__":
    build_gold_warehouse()
