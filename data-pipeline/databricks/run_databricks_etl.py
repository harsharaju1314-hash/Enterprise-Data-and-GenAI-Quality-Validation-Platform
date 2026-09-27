"""
Databricks ETL Pipeline Runner
Executes bronze -> silver -> gold transformations and populates relational tables.
"""

import os
import sys
import sqlite3
import pandas as pd
import importlib.util

current_dir = os.path.dirname(os.path.abspath(__file__))

def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

mod_silver = import_module_from_file("bronze_to_silver_cleaning", os.path.join(current_dir, "01_bronze_to_silver_cleaning.py"))
mod_gold = import_module_from_file("silver_to_gold_aggregates", os.path.join(current_dir, "02_silver_to_gold_aggregates.py"))

clean_customers = mod_silver.clean_customers
clean_service_requests = mod_silver.clean_service_requests
clean_transactions = mod_silver.clean_transactions

generate_customer_metrics = mod_gold.generate_customer_metrics
generate_category_summary = mod_gold.generate_category_summary
generate_financial_daily_metrics = mod_gold.generate_financial_daily_metrics

def execute_etl(base_dir=None):
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    raw_dir = os.path.join(base_dir, "test-data", "raw_blob")
    silver_dir = os.path.join(base_dir, "data-pipeline", "silver")
    gold_dir = os.path.join(base_dir, "data-pipeline", "gold")
    db_path = os.path.join(base_dir, "data-pipeline", "enterprise_analytics.db")
    
    os.makedirs(silver_dir, exist_ok=True)
    os.makedirs(gold_dir, exist_ok=True)
    
    print(f"[*] Reading Raw Bronze Data from {raw_dir}...")
    df_raw_cust = pd.read_csv(os.path.join(raw_dir, "customers.csv"))
    df_raw_sr = pd.read_csv(os.path.join(raw_dir, "service_requests.csv"))
    df_raw_txn = pd.read_csv(os.path.join(raw_dir, "transactions.csv"))
    
    print(f"[*] Executing Bronze -> Silver Transformations...")
    df_silver_cust = clean_customers(df_raw_cust)
    df_silver_sr = clean_service_requests(df_raw_sr)
    df_silver_txn = clean_transactions(df_raw_txn)
    
    # Save Silver datasets
    df_silver_cust.to_csv(os.path.join(silver_dir, "dim_customers.csv"), index=False)
    df_silver_sr.to_csv(os.path.join(silver_dir, "fact_service_requests.csv"), index=False)
    df_silver_txn.to_csv(os.path.join(silver_dir, "fact_transactions.csv"), index=False)
    print("    [OK] Saved Silver CSVs")
    
    print(f"[*] Executing Silver -> Gold Aggregations...")
    df_gold_cust = generate_customer_metrics(df_silver_cust, df_silver_sr, df_silver_txn)
    df_gold_cat = generate_category_summary(df_silver_sr)
    df_gold_fin = generate_financial_daily_metrics(df_silver_txn)
    
    # Save Gold datasets
    df_gold_cust.to_csv(os.path.join(gold_dir, "agg_customer_360.csv"), index=False)
    df_gold_cat.to_csv(os.path.join(gold_dir, "agg_category_summary.csv"), index=False)
    df_gold_fin.to_csv(os.path.join(gold_dir, "agg_financial_daily.csv"), index=False)
    print("    [OK] Saved Gold CSVs")
    
    print(f"[*] Loading into Relational Database at {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Write tables
    df_silver_cust.to_sql("dim_customers", conn, if_exists="replace", index=False)
    df_silver_sr.to_sql("fact_service_requests", conn, if_exists="replace", index=False)
    df_silver_txn.to_sql("fact_transactions", conn, if_exists="replace", index=False)
    df_gold_cust.to_sql("agg_customer_360", conn, if_exists="replace", index=False)
    df_gold_cat.to_sql("agg_category_summary", conn, if_exists="replace", index=False)
    df_gold_fin.to_sql("agg_financial_daily", conn, if_exists="replace", index=False)
    
    conn.commit()
    conn.close()
    print("    [OK] Relational Tables Populated Successfully")
    return True

if __name__ == "__main__":
    execute_etl()
