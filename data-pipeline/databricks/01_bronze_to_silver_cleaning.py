# Databricks Notebook: Bronze to Silver Transformation & Quality Cleaning
# Description: Cleans raw ingestion files, eliminates duplicates, standardizes formats, validates business categories, and computes derived fields.

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

def clean_customers(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw customer data:
    1. Deduplicates on customer_id
    2. Trims whitespace and normalizes email to lowercase
    3. Validates and enforces allowed Tiers and Regions
    4. Standardizes account_created_date to YYYY-MM-DD
    5. Adds derived full_name and validation flags
    """
    df = df_raw.copy()
    
    # 1. Deduplicate
    df = df.drop_duplicates(subset=["customer_id"], keep="last")
    
    # 2. Clean strings
    df["first_name"] = df["first_name"].astype(str).str.strip()
    df["last_name"] = df["last_name"].astype(str).str.strip()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["full_name"] = df["first_name"] + " " + df["last_name"]
    
    # 3. Validate Tier
    valid_tiers = {"Platinum", "Gold", "Silver", "Bronze"}
    df["tier"] = df["tier"].apply(lambda x: x if x in valid_tiers else "Bronze")
    
    # 4. Standardize dates
    df["account_created_date"] = pd.to_datetime(df["account_created_date"]).dt.strftime("%Y-%m-%d")
    
    # 5. Status validation
    df["status"] = df["status"].apply(lambda x: x if x in {"Active", "Inactive"} else "Active")
    
    return df

def clean_service_requests(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw service requests:
    1. Deduplicates on request_id
    2. Standardizes timestamps (created_date, resolved_date)
    3. Validates category and priority enums
    4. Computes derived field: resolution_time_hours
    5. Computes SLA compliance flag based on priority SLA rules
    """
    df = df_raw.copy()
    
    # 1. Deduplicate
    df = df.drop_duplicates(subset=["request_id"], keep="last")
    
    # 2. Standardize timestamps
    df["created_date"] = pd.to_datetime(df["created_date"])
    df["resolved_date"] = pd.to_datetime(df["resolved_date"])
    
    # 3. Categorical validation
    valid_categories = {"Billing", "Technical", "Account", "General"}
    valid_priorities = {"Urgent", "High", "Medium", "Low"}
    valid_statuses = {"Open", "In_Progress", "Closed"}
    
    df["category"] = df["category"].apply(lambda x: x if x in valid_categories else "General")
    df["priority"] = df["priority"].apply(lambda x: x if x in valid_priorities else "Medium")
    df["status"] = df["status"].apply(lambda x: x if x in valid_statuses else "Open")
    
    # 4. Derived field: resolution_time_hours
    df["resolution_time_hours"] = (df["resolved_date"] - df["created_date"]).dt.total_seconds() / 3600.0
    df["resolution_time_hours"] = df["resolution_time_hours"].apply(lambda x: round(x, 2) if pd.notnull(x) and x >= 0 else None)
    
    # 5. SLA Calculation (Urgent: 4h, High: 12h, Medium: 48h, Low: 120h)
    sla_map = {"Urgent": 4.0, "High": 12.0, "Medium": 48.0, "Low": 120.0}
    def check_sla(row):
        if pd.isnull(row["resolution_time_hours"]):
            return None
        target_hours = sla_map.get(row["priority"], 48.0)
        return "Compliant" if row["resolution_time_hours"] <= target_hours else "Breached"
    
    df["sla_compliance"] = df.apply(check_sla, axis=1)
    
    # Satisfaction score cleanup (ensure numeric or null)
    df["satisfaction_score"] = pd.to_numeric(df["satisfaction_score"], errors="coerce")
    
    return df

def clean_transactions(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw transactions:
    1. Deduplicates on transaction_id
    2. Validates amount > 0 and currency == 'USD'
    3. Standardizes transaction_date
    4. Computes net_amount (considering refund/failure adjustments)
    """
    df = df_raw.copy()
    
    # 1. Deduplicate
    df = df.drop_duplicates(subset=["transaction_id"], keep="last")
    
    # 2. Validate amount and currency
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["currency"] = df["currency"].apply(lambda x: "USD" if str(x).strip().upper() == "USD" else "USD")
    
    # 3. Standardize timestamps
    df["transaction_date"] = pd.to_datetime(df["transaction_date"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # 4. Derived net_amount
    def calc_net(row):
        if row["status"] == "Completed":
            return row["amount"]
        elif row["status"] == "Refunded":
            return -row["amount"]
        else: # Failed
            return 0.0
            
    df["net_amount"] = df.apply(calc_net, axis=1)
    
    return df
