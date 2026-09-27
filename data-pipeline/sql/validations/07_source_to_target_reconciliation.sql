-- ==========================================================
-- 07. SOURCE-TO-TARGET RECONCILIATION
-- Purpose: Verify record counts, volume totals, and key metrics across pipeline stages.
-- ==========================================================

-- Stage 1: Customers Row Count Reconciliation
-- Expected Source Count: 12 -> Target dim_customers Count: 12
SELECT 'RECON_CUSTOMER_COUNT' AS test_name,
       COUNT(*) AS target_count,
       12 AS expected_source_count,
       CASE WHEN COUNT(*) = 12 THEN 'PASS' ELSE 'FAIL' END AS status
FROM dim_customers;

-- Stage 2: Service Requests Row Count Reconciliation
-- Expected Source Count: 15 -> Target fact_service_requests Count: 15
SELECT 'RECON_SERVICE_REQUESTS_COUNT' AS test_name,
       COUNT(*) AS target_count,
       15 AS expected_source_count,
       CASE WHEN COUNT(*) = 15 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_service_requests;

-- Stage 3: Transactions Row Count Reconciliation
-- Expected Source Count: 16 -> Target fact_transactions Count: 16
SELECT 'RECON_TRANSACTIONS_COUNT' AS test_name,
       COUNT(*) AS target_count,
       16 AS expected_source_count,
       CASE WHEN COUNT(*) = 16 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_transactions;

-- Stage 4: Financial Gross Volume Reconciliation
-- Expected Gross Volume (sum of all 16 rows): $5,049.74
SELECT 'RECON_TRANSACTION_GROSS_VOLUME' AS test_name,
       ROUND(SUM(amount), 2) AS target_gross_volume,
       5049.74 AS expected_source_gross_volume,
       CASE WHEN ROUND(SUM(amount), 2) = 5049.74 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_transactions;

-- Stage 5: Financial Completed Volume Reconciliation
-- Expected Completed Gross Volume: 14 completed txns = $4,879.49
SELECT 'RECON_TRANSACTION_COMPLETED_VOLUME' AS test_name,
       ROUND(SUM(amount), 2) AS target_completed_volume,
       4879.49 AS expected_completed_volume,
       CASE WHEN ROUND(SUM(amount), 2) = 4879.49 THEN 'PASS' ELSE 'FAIL' END AS status
FROM fact_transactions
WHERE status = 'Completed';
