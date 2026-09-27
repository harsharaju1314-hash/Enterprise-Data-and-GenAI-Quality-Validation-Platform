# Test Cases: Cloud Data Pipeline & Data Quality

| Test Case ID | Test Title | Dimension | Pre-conditions | Test Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-DATA-01** | Mandatory Null Check on Customers | Completeness | Silver table populated | Run query checking nulls in `customer_id`, `email`, `tier` | 0 null records found | **PASS** |
| **TC-DATA-02** | Mandatory Null Check on Service Requests | Completeness | Silver table populated | Check nulls in `request_id`, `category`, `priority`, `created_date` | 0 null records found | **PASS** |
| **TC-DATA-03** | Mandatory Null Check on Transactions | Completeness | Silver table populated | Check nulls in `transaction_id`, `amount`, `status` | 0 null records found | **PASS** |
| **TC-DATA-04** | Resolution Time Non-Negative Check | Accuracy | Silver table populated | Check for `resolution_time_hours < 0` in closed tickets | 0 records with negative duration | **PASS** |
| **TC-DATA-05** | Transaction Net Amount Calculation | Accuracy | Silver table populated | Verify Completed = amount, Refunded = -amount, Failed = 0 | 100% mathematical match | **PASS** |
| **TC-DATA-06** | Service Request Referential Integrity | Consistency | Dimension & Fact populated | Left join service requests to customers; check null parent | 0 orphan service requests | **PASS** |
| **TC-DATA-07** | Transaction Referential Integrity | Consistency | Dimension & Fact populated | Left join transactions to customers; check null parent | 0 orphan transactions | **PASS** |
| **TC-DATA-08** | Customer ID Uniqueness | Uniqueness | Silver table populated | Group by `customer_id` HAVING count > 1 | 0 duplicate keys | **PASS** |
| **TC-DATA-09** | Request ID Uniqueness | Uniqueness | Silver table populated | Group by `request_id` HAVING count > 1 | 0 duplicate keys | **PASS** |
| **TC-DATA-10** | Transaction ID Uniqueness | Uniqueness | Silver table populated | Group by `transaction_id` HAVING count > 1 | 0 duplicate keys | **PASS** |
| **TC-DATA-11** | Customer Tier Allowed Values | Validity | Silver table populated | Verify `tier IN ('Platinum', 'Gold', 'Silver', 'Bronze')` | 0 invalid tier records | **PASS** |
| **TC-DATA-12** | Request Category Allowed Values | Validity | Silver table populated | Verify `category IN ('Billing', 'Technical', 'Account', 'General')` | 0 invalid category records | **PASS** |
| **TC-DATA-13** | CSAT Score Range 1 to 5 | Validity | Silver table populated | Verify `satisfaction_score BETWEEN 1 AND 5` | 0 scores outside range | **PASS** |
| **TC-DATA-14** | Chronological Ordering Check | Timeliness | Silver table populated | Check `resolved_date >= created_date` | 0 chronology violations | **PASS** |
| **TC-DATA-15** | Source-to-Target Customer Count | Reconciliation | Raw CSV & SQL table | Compare row count of `customers.csv` vs `dim_customers` | Exactly 12 rows in both | **PASS** |
| **TC-DATA-16** | Source-to-Target Request Count | Reconciliation | Raw CSV & SQL table | Compare row count of `service_requests.csv` vs `fact_service_requests` | Exactly 15 rows in both | **PASS** |
| **TC-DATA-17** | Source-to-Target Transaction Count | Reconciliation | Raw CSV & SQL table | Compare row count of `transactions.csv` vs `fact_transactions` | Exactly 16 rows in both | **PASS** |
| **TC-DATA-18** | Gross Transaction Volume Reconciliation | Reconciliation | Raw CSV & SQL table | Compare sum of amounts across raw CSV and SQL table | Exactly \$5,049.74 in both | **PASS** |
| **TC-DATA-19** | Completed Transaction Volume Reconciliation | Reconciliation | Raw CSV & SQL table | Compare sum of completed transactions in raw vs SQL | Exactly \$4,879.49 in both | **PASS** |
