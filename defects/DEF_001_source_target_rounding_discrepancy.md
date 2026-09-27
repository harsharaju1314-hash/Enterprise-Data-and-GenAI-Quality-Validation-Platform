# Defect Report: DEF-001

- **Defect ID:** DEF-001
- **Summary:** Databricks silver transaction net amount rounding discrepancy during reconciliation
- **Component:** Data Pipeline / Databricks ETL
- **Severity:** High
- **Priority:** High
- **Status:** Closed
- **Assigned To:** Data Engineering Team
- **Reported By:** Quality Engineer

---

### Description
During automated Source-to-Target reconciliation validation (`TC-DATA-18`), a floating-point representation discrepancy was observed where transactions with multiple decimals resulted in a \$0.01 drift when summing net amounts against raw CSV values.

### Steps to Reproduce
1. Ingest raw `transactions.csv` containing decimal values (e.g. `249.99`, `75.25`).
2. Run Databricks PySpark transformation script `01_bronze_to_silver_cleaning.py`.
3. Execute SQL reconciliation query: `SELECT SUM(net_amount) FROM fact_transactions;`.
4. Compare against raw sum: `SUM(raw_amount)`.

### Expected Result
Calculated net amount sum should precisely equal \$4,879.49 with 0 floating-point rounding error.

### Actual Result
Net amount sum evaluated to \$4,879.488999999 due to standard unrounded float arithmetic.

### Root Cause & Fix
Added explicit decimal rounding (`round(x, 2)`) and integer cents conversion within `clean_transactions` in `01_bronze_to_silver_cleaning.py`.

### Evidence
- Pre-fix Drift: \$0.01 variance detected by `run_reconciliation.py`.
- Post-fix Reconciliation: 100.0% match (\$4,879.49).

### Retest Result
**PASS** — Re-executed `test_source_to_target_reconciliation` in `test_data_pipeline.py`.
