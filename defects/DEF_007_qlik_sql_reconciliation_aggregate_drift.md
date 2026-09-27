# Defect Report: DEF-007

- **Defect ID:** DEF-007
- **Summary:** Qlik Sense dashboard Gross Volume included refunded amounts without net revenue separation
- **Component:** Qlik Sense Analytics / KPI Definitions
- **Severity:** High
- **Priority:** Medium
- **Status:** Closed
- **Assigned To:** BI / Analytics Developer
- **Reported By:** Quality Engineer

---

### Description
Independent SQL reconciliation query (`dashboard_reconciliation.sql`) revealed that the Qlik Sense Master Measure for Gross Volume was displaying \$5,049.74 without distinguishing completed vs refunded orders, inflating executive revenue metrics.

### Steps to Reproduce
1. Open Qlik Sense dashboard.
2. Compare Gross Volume KPI vs Net Revenue KPI.
3. Compare against SQL query:
   ```sql
   SELECT SUM(amount) as gross, SUM(net_amount) as net FROM fact_transactions;
   ```

### Expected Result
Dashboard explicitly provides separate Master Items for `Gross Volume` (\$5,049.74) and `Net Revenue` (\$4,763.49).

### Actual Result
Single gross volume metric was labeled "Total Revenue" causing confusion.

### Root Cause & Fix
Updated `app_load_script.qvs` and dashboard layout to define separate Master Measures for Gross Volume and Net Revenue.

### Retest Result
**PASS** — Verified with `TC-QLIK-01` and SQL reconciliation suite.
