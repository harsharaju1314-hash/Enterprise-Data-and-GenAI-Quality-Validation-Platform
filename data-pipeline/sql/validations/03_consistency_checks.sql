-- ==========================================================
-- 03. CONSISTENCY CHECKS
-- Purpose: Verify referential integrity and logical consistency across related tables.
-- ==========================================================

-- Check 3.1: Orphaned Service Requests (foreign key consistency)
SELECT 'ORPHAN_SERVICE_REQUESTS' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests sr
LEFT JOIN dim_customers c ON sr.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Check 3.2: Orphaned Transactions (foreign key consistency)
SELECT 'ORPHAN_TRANSACTIONS' AS test_name, COUNT(*) AS failure_count
FROM fact_transactions t
LEFT JOIN dim_customers c ON t.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Check 3.3: Total open + closed service requests in Customer 360 equals total service requests
SELECT 'CUSTOMER_360_SR_SUM_CONSISTENCY' AS test_name, COUNT(*) AS failure_count
FROM agg_customer_360
WHERE (open_service_requests + closed_service_requests) != total_service_requests;
