-- ==========================================================
-- 04. UNIQUENESS CHECKS
-- Purpose: Verify entity primary key uniqueness across dimension and fact tables.
-- ==========================================================

-- Check 4.1: Customer ID Uniqueness
SELECT 'CUST_DUPLICATE_KEY' AS test_name, COUNT(*) AS failure_count
FROM (
    SELECT customer_id, COUNT(*) AS cnt
    FROM dim_customers
    GROUP BY customer_id
    HAVING COUNT(*) > 1
);

-- Check 4.2: Service Request ID Uniqueness
SELECT 'SR_DUPLICATE_KEY' AS test_name, COUNT(*) AS failure_count
FROM (
    SELECT request_id, COUNT(*) AS cnt
    FROM fact_service_requests
    GROUP BY request_id
    HAVING COUNT(*) > 1
);

-- Check 4.3: Transaction ID Uniqueness
SELECT 'TXN_DUPLICATE_KEY' AS test_name, COUNT(*) AS failure_count
FROM (
    SELECT transaction_id, COUNT(*) AS cnt
    FROM fact_transactions
    GROUP BY transaction_id
    HAVING COUNT(*) > 1
);
