# Defect Report: DEF-002

- **Defect ID:** DEF-002
- **Summary:** Closed service requests persisted with NULL resolved date violating schema integrity
- **Component:** Data Pipeline / Azure SQL Schema
- **Severity:** Critical
- **Priority:** High
- **Status:** Closed
- **Assigned To:** Data Engineering Team
- **Reported By:** Quality Engineer

---

### Description
Data quality completeness check (`01_completeness_checks.sql`) flagged records in `fact_service_requests` where `status = 'Closed'` but `resolved_date` was stored as `NULL`, violating the business rule that all closed tickets must have an immutable resolution timestamp.

### Steps to Reproduce
1. Ingest service requests where raw input had status `Closed` but blank `resolved_date`.
2. Execute SQL quality check:
   ```sql
   SELECT COUNT(*) FROM fact_service_requests WHERE status = 'Closed' AND (resolved_date IS NULL OR resolved_date = '');
   ```

### Expected Result
Transformation pipeline should either impute the batch timestamp or reject incomplete records into a dead-letter error queue.

### Actual Result
Null timestamps were written directly to the target analytics table, skewing average resolution time calculations.

### Root Cause & Fix
Updated Databricks notebook `01_bronze_to_silver_cleaning.py` to enforce fallback timestamp derivation and schema check constraints.

### Retest Result
**PASS** — Re-executed `validate_completeness()` with 0 failures recorded.
