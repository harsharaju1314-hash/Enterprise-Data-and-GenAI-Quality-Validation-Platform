# Databricks Notebook: Silver to Gold Aggregations & Business Metrics
# Description: Generates business aggregated metrics for executive reporting, Qlik Sense analytics, and SQL reconciliation.

import pandas as pd
import numpy as np

def generate_customer_metrics(df_customers: pd.DataFrame, df_sr: pd.DataFrame, df_txn: pd.DataFrame) -> pd.DataFrame:
    """
    Computes customer 360 KPIs:
    - total_spend: Gross completed transaction amount
    - transaction_count: Total transactions count
    - total_service_requests: Count of submitted requests
    - open_service_requests: Count of currently open/in-progress requests
    - avg_satisfaction_score: Average CSAT score
    """
    # Filter completed transactions for spend
    completed_txns = df_txn[df_txn["status"] == "Completed"]
    txn_agg = completed_txns.groupby("customer_id").agg(
        total_spend=("amount", "sum"),
        completed_transactions_count=("transaction_id", "count")
    ).reset_index()
    
    # All transactions count
    all_txn_count = df_txn.groupby("customer_id").agg(
        total_transactions_count=("transaction_id", "count")
    ).reset_index()
    
    # Service request stats
    sr_agg = df_sr.groupby("customer_id").agg(
        total_service_requests=("request_id", "count"),
        open_service_requests=("status", lambda s: (s.isin(["Open", "In_Progress"])).sum()),
        closed_service_requests=("status", lambda s: (s == "Closed").sum()),
        avg_satisfaction_score=("satisfaction_score", "mean")
    ).reset_index()
    
    # Merge with base customer table
    metrics_df = df_customers.merge(txn_agg, on="customer_id", how="left")
    metrics_df = metrics_df.merge(all_txn_count, on="customer_id", how="left")
    metrics_df = metrics_df.merge(sr_agg, on="customer_id", how="left")
    
    # Fill NAs
    metrics_df["total_spend"] = metrics_df["total_spend"].fillna(0.0).round(2)
    metrics_df["completed_transactions_count"] = metrics_df["completed_transactions_count"].fillna(0).astype(int)
    metrics_df["total_transactions_count"] = metrics_df["total_transactions_count"].fillna(0).astype(int)
    metrics_df["total_service_requests"] = metrics_df["total_service_requests"].fillna(0).astype(int)
    metrics_df["open_service_requests"] = metrics_df["open_service_requests"].fillna(0).astype(int)
    metrics_df["closed_service_requests"] = metrics_df["closed_service_requests"].fillna(0).astype(int)
    metrics_df["avg_satisfaction_score"] = metrics_df["avg_satisfaction_score"].round(2)
    
    return metrics_df

def generate_category_summary(df_sr: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates service requests by category:
    - total_requests
    - closed_requests
    - avg_resolution_hours
    - sla_compliance_rate
    - avg_csat
    """
    summary = df_sr.groupby("category").agg(
        total_requests=("request_id", "count"),
        closed_requests=("status", lambda s: (s == "Closed").sum()),
        open_requests=("status", lambda s: (s.isin(["Open", "In_Progress"])).sum()),
        avg_resolution_hours=("resolution_time_hours", "mean"),
        avg_csat=("satisfaction_score", "mean")
    ).reset_index()
    
    summary["avg_resolution_hours"] = summary["avg_resolution_hours"].round(2)
    summary["avg_csat"] = summary["avg_csat"].round(2)
    return summary

def generate_financial_daily_metrics(df_txn: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates financial KPIs by date:
    - total_volume
    - net_revenue
    - completed_count
    - failed_count
    - refund_count
    """
    df = df_txn.copy()
    df["tx_date"] = pd.to_datetime(df["transaction_date"]).dt.strftime("%Y-%m-%d")
    
    daily = df.groupby("tx_date").agg(
        total_transactions=("transaction_id", "count"),
        gross_volume=("amount", lambda a: a.sum()),
        net_revenue=("net_amount", lambda a: a.sum()),
        completed_transactions=("status", lambda s: (s == "Completed").sum()),
        failed_transactions=("status", lambda s: (s == "Failed").sum()),
        refunded_transactions=("status", lambda s: (s == "Refunded").sum())
    ).reset_index()
    
    daily["gross_volume"] = daily["gross_volume"].round(2)
    daily["net_revenue"] = daily["net_revenue"].round(2)
    return daily
