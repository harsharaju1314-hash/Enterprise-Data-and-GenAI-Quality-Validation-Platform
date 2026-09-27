"""
Data Quality Validation Engine
Executes automated quality checks across 7 dimensions and generates test reports.
"""

import os
import sqlite3
import pandas as pd
from typing import Dict, List, Any

class DataQualityEngine:
    def __init__(self, db_path: str = None):
        if db_path is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            self.db_path = os.path.join(base_dir, "data-pipeline", "enterprise_analytics.db")
        else:
            self.db_path = db_path
            
    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def run_query(self, query: str) -> pd.DataFrame:
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn)

    def validate_completeness(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("dim_customers Mandatory Null Check", "SELECT COUNT(*) as count FROM dim_customers WHERE customer_id IS NULL OR email IS NULL OR tier IS NULL;"),
            ("fact_service_requests Mandatory Null Check", "SELECT COUNT(*) as count FROM fact_service_requests WHERE request_id IS NULL OR customer_id IS NULL OR category IS NULL OR priority IS NULL;"),
            ("fact_transactions Mandatory Null Check", "SELECT COUNT(*) as count FROM fact_transactions WHERE transaction_id IS NULL OR customer_id IS NULL OR amount IS NULL OR status IS NULL;")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Completeness",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_accuracy(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("Resolution Time Non-Negative Check", "SELECT COUNT(*) as count FROM fact_service_requests WHERE status = 'Closed' AND resolution_time_hours < 0;"),
            ("Transaction Net Amount Logic Check", "SELECT COUNT(*) as count FROM fact_transactions WHERE (status = 'Completed' AND net_amount != amount) OR (status = 'Refunded' AND net_amount != -amount) OR (status = 'Failed' AND net_amount != 0);")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Accuracy",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_consistency(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("Service Request Orphan Check", "SELECT COUNT(*) as count FROM fact_service_requests sr LEFT JOIN dim_customers c ON sr.customer_id = c.customer_id WHERE c.customer_id IS NULL;"),
            ("Transaction Orphan Check", "SELECT COUNT(*) as count FROM fact_transactions t LEFT JOIN dim_customers c ON t.customer_id = c.customer_id WHERE c.customer_id IS NULL;")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Consistency",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_uniqueness(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("Customer ID Duplicate Check", "SELECT COUNT(*) as count FROM (SELECT customer_id FROM dim_customers GROUP BY customer_id HAVING COUNT(*) > 1);"),
            ("Request ID Duplicate Check", "SELECT COUNT(*) as count FROM (SELECT request_id FROM fact_service_requests GROUP BY request_id HAVING COUNT(*) > 1);"),
            ("Transaction ID Duplicate Check", "SELECT COUNT(*) as count FROM (SELECT transaction_id FROM fact_transactions GROUP BY transaction_id HAVING COUNT(*) > 1);")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Uniqueness",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_validity(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("Customer Tier Allowed Values", "SELECT COUNT(*) as count FROM dim_customers WHERE tier NOT IN ('Platinum', 'Gold', 'Silver', 'Bronze');"),
            ("Service Request Category Allowed Values", "SELECT COUNT(*) as count FROM fact_service_requests WHERE category NOT IN ('Billing', 'Technical', 'Account', 'General');"),
            ("CSAT Range 1 to 5 Check", "SELECT COUNT(*) as count FROM fact_service_requests WHERE satisfaction_score IS NOT NULL AND (satisfaction_score < 1 OR satisfaction_score > 5);")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Validity",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_timeliness(self) -> List[Dict[str, Any]]:
        results = []
        checks = [
            ("Resolved Date >= Created Date Chronology", "SELECT COUNT(*) as count FROM fact_service_requests WHERE resolved_date IS NOT NULL AND resolved_date < created_date;"),
            ("Fresh Active Period Records Check", "SELECT CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END as count FROM fact_transactions WHERE transaction_date >= '2025-08-01';")
        ]
        for name, sql in checks:
            df = self.run_query(sql)
            count = int(df["count"].iloc[0])
            results.append({
                "dimension": "Timeliness",
                "check_name": name,
                "failures": count,
                "status": "PASS" if count == 0 else "FAIL"
            })
        return results

    def validate_reconciliation(self, raw_blob_dir: str = None) -> List[Dict[str, Any]]:
        results = []
        if raw_blob_dir is None:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            raw_blob_dir = os.path.join(base_dir, "test-data", "raw_blob")
            
        df_raw_cust = pd.read_csv(os.path.join(raw_blob_dir, "customers.csv"))
        df_raw_sr = pd.read_csv(os.path.join(raw_blob_dir, "service_requests.csv"))
        df_raw_txn = pd.read_csv(os.path.join(raw_blob_dir, "transactions.csv"))
        
        # Recon 1: Customers
        sql_cust_cnt = int(self.run_query("SELECT COUNT(*) as count FROM dim_customers;")["count"].iloc[0])
        results.append({
            "dimension": "Reconciliation",
            "check_name": "Source Customers vs Target dim_customers Count",
            "source_val": len(df_raw_cust),
            "target_val": sql_cust_cnt,
            "status": "PASS" if len(df_raw_cust) == sql_cust_cnt else "FAIL"
        })
        
        # Recon 2: Service Requests
        sql_sr_cnt = int(self.run_query("SELECT COUNT(*) as count FROM fact_service_requests;")["count"].iloc[0])
        results.append({
            "dimension": "Reconciliation",
            "check_name": "Source Service Requests vs Target fact_service_requests Count",
            "source_val": len(df_raw_sr),
            "target_val": sql_sr_cnt,
            "status": "PASS" if len(df_raw_sr) == sql_sr_cnt else "FAIL"
        })
        
        # Recon 3: Transactions Count & Gross Volume
        sql_txn_cnt = int(self.run_query("SELECT COUNT(*) as count FROM fact_transactions;")["count"].iloc[0])
        sql_txn_gross = round(float(self.run_query("SELECT SUM(amount) as gross FROM fact_transactions;")["gross"].iloc[0]), 2)
        raw_txn_gross = round(float(df_raw_txn["amount"].sum()), 2)
        
        results.append({
            "dimension": "Reconciliation",
            "check_name": "Source Transactions vs Target fact_transactions Count",
            "source_val": len(df_raw_txn),
            "target_val": sql_txn_cnt,
            "status": "PASS" if len(df_raw_txn) == sql_txn_cnt else "FAIL"
        })
        results.append({
            "dimension": "Reconciliation",
            "check_name": "Source Transaction Gross Volume vs Target Gross Volume",
            "source_val": raw_txn_gross,
            "target_val": sql_txn_gross,
            "status": "PASS" if raw_txn_gross == sql_txn_gross else "FAIL"
        })
        
        return results

    def run_all_validations(self) -> Dict[str, Any]:
        report = {
            "Completeness": self.validate_completeness(),
            "Accuracy": self.validate_accuracy(),
            "Consistency": self.validate_consistency(),
            "Uniqueness": self.validate_uniqueness(),
            "Validity": self.validate_validity(),
            "Timeliness": self.validate_timeliness(),
            "Reconciliation": self.validate_reconciliation()
        }
        
        total_checks = sum(len(v) for v in report.values())
        passed_checks = sum(sum(1 for item in v if item["status"] == "PASS") for v in report.values())
        failed_checks = total_checks - passed_checks
        
        return {
            "summary": {
                "total_checks": total_checks,
                "passed": passed_checks,
                "failed": failed_checks,
                "pass_rate_pct": round((passed_checks / total_checks) * 100, 2)
            },
            "details": report
        }
