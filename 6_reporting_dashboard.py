"""
Step 6: Reporting, Dashboard & Power BI Export
=============================================
Purpose:
  - Connects to the Gold SQLite database (data/gold/sales_warehouse.db).
  - Generates key business KPIs and reporting insights in the terminal.
  - Exports business-ready Gold datasets to CSV files for seamless 1-click Power BI import.
"""

import os
import sqlite3
import pandas as pd

# File paths
GOLD_DB_PATH = os.path.join("data", "gold", "sales_warehouse.db")
POWERBI_FACT_CSV = os.path.join("data", "gold", "powerbi_fact_sales.csv")
POWERBI_CATEGORY_CSV = os.path.join("data", "gold", "powerbi_category_summary.csv")


def generate_reports():
    """Reads Gold data warehouse and produces summary analytics and Power BI export files."""
    
    if not os.path.exists(GOLD_DB_PATH):
        print(f"[Error] Gold database not found at '{GOLD_DB_PATH}'.")
        print("Please run Step 5 (Gold Warehouse) first.")
        return

    print("=" * 60)
    print("Executive Sales Reporting & Power BI Export")
    print("=" * 60)

    # 1. Connect to SQLite Gold Database
    conn = sqlite3.connect(GOLD_DB_PATH)

    # 2. Load Fact and Summary Tables
    df_fact = pd.read_sql_query("SELECT * FROM fact_sales_orders", conn)
    df_category = pd.read_sql_query("SELECT * FROM agg_category_sales", conn)

    # 3. Calculate Executive KPIs
    total_revenue = df_fact["total_amount"].sum()
    total_orders = len(df_fact)
    avg_order_val = df_fact["total_amount"].mean()
    top_category = df_category.sort_values(by="total_revenue", ascending=False).iloc[0]

    print("\n--- Key Business KPIs ---")
    print(f"Total Revenue       : ${total_revenue:,.2f}")
    print(f"Total Orders        : {total_orders}")
    print(f"Average Order Value : ${avg_order_val:,.2f}")
    print(f"Top Category        : {top_category['category']} (${top_category['total_revenue']:,.2f})")

    # 4. Breakdown by City
    print("\n--- Revenue by City ---")
    city_summary = df_fact.groupby("city")["total_amount"].sum().reset_index().rename(columns={"total_amount": "revenue"})
    print(city_summary.to_string(index=False))

    # 5. Breakdown by Order Status
    print("\n--- Orders by Status ---")
    status_summary = df_fact["status"].value_counts().reset_index()
    status_summary.columns = ["status", "order_count"]
    print(status_summary.to_string(index=False))

    # 6. Export datasets for Power BI
    df_fact.to_csv(POWERBI_FACT_CSV, index=False)
    df_category.to_csv(POWERBI_CATEGORY_CSV, index=False)
    
    conn.close()

    print("\n" + "=" * 60)
    print("[SUCCESS] Power BI datasets exported:")
    print(f"  1. Fact Sales Table       -> {POWERBI_FACT_CSV}")
    print(f"  2. Category Summary Table -> {POWERBI_CATEGORY_CSV}")
    print("=" * 60)


if __name__ == "__main__":
    generate_reports()
