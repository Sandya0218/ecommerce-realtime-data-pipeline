"""
Step 4: ETL / Data Processing (Silver Layer)
============================================
Purpose:
  - Reads raw JSON data from the Bronze layer (data/bronze/bronze_orders.json).
  - Cleans and transforms the data (removes duplicates, fixes data types, validates values).
  - Saves the cleaned, structured tabular data to the Silver layer (data/silver/silver_orders.csv).
"""

import os
import pandas as pd

# File paths
BRONZE_FILE_PATH = os.path.join("data", "bronze", "bronze_orders.json")
SILVER_FILE_PATH = os.path.join("data", "silver", "silver_orders.csv")


def process_bronze_to_silver():
    """Reads Bronze data, cleans and standardizes it, and saves to Silver layer."""
    
    # 1. Check if Bronze file exists
    if not os.path.exists(BRONZE_FILE_PATH):
        print(f"[Error] Bronze file not found at '{BRONZE_FILE_PATH}'.")
        print("Please run Step 2 (Producer) and Step 3 (Consumer) first to generate bronze data.")
        return

    print("=" * 60)
    print("Starting Silver Layer ETL Transformation")
    print("=" * 60)

    # 2. Read Bronze JSON Lines into a Pandas DataFrame
    print(f"Reading raw data from: {BRONZE_FILE_PATH}")
    df = pd.read_json(BRONZE_FILE_PATH, lines=True)
    raw_count = len(df)
    print(f"Loaded {raw_count} raw records from Bronze layer.")

    if raw_count == 0:
        print("[Notice] Bronze file is empty. Nothing to process.")
        return

    # 3. Data Cleaning: Remove duplicates based on order_id
    df = df.drop_duplicates(subset=["order_id"], keep="last")
    dedup_count = len(df)
    print(f"Removed {raw_count - dedup_count} duplicate record(s).")

    # 4. Data Cleaning: Drop rows with missing critical fields
    df = df.dropna(subset=["order_id", "customer_id", "product", "price", "quantity"])

    # 5. Data Type Standardization
    df["order_id"] = df["order_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["price"] = df["price"].astype(float)
    df["total_amount"] = (df["quantity"] * df["price"]).round(2)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Standardize string fields (remove extra whitespace)
    str_cols = ["customer_id", "product", "category", "payment_method", "city", "status"]
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 6. Ensure Silver destination folder exists
    os.makedirs(os.path.dirname(SILVER_FILE_PATH), exist_ok=True)

    # 7. Save cleaned data to Silver CSV
    df.to_csv(SILVER_FILE_PATH, index=False)
    print(f"Successfully saved {len(df)} cleaned records to: {SILVER_FILE_PATH}")

    # 8. Print preview of cleaned Silver dataset
    print("\n--- Preview of Silver Layer Data ---")
    print(df.head())
    print("\n[SUCCESS] Step 4 Silver ETL completed successfully!")


if __name__ == "__main__":
    process_bronze_to_silver()
