-- ==========================================================
-- 01. COMPLETENESS CHECKS
-- Purpose: Verify mandatory fields are non-null and no records are orphaned.
-- ==========================================================

-- Check 1.1: Missing mandatory fields in dim_customers
SELECT 'CUST_NULL_CHECK' AS test_name, COUNT(*) AS failure_count
FROM dim_customers
WHERE customer_id IS NULL OR email IS NULL OR tier IS NULL OR region IS NULL;

-- Check 1.2: Missing mandatory fields in fact_service_requests
SELECT 'SR_NULL_CHECK' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE request_id IS NULL OR customer_id IS NULL OR category IS NULL OR priority IS NULL OR created_date IS NULL;

-- Check 1.3: Missing mandatory fields in fact_transactions
SELECT 'TXN_NULL_CHECK' AS test_name, COUNT(*) AS failure_count
FROM fact_transactions
WHERE transaction_id IS NULL OR customer_id IS NULL OR transaction_date IS NULL OR amount IS NULL OR status IS NULL;

-- Check 1.4: Closed tickets with missing resolution dates
SELECT 'CLOSED_TICKETS_MISSING_RESOLVED_DATE' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE status = 'Closed' AND (resolved_date IS NULL OR resolved_date = '');
