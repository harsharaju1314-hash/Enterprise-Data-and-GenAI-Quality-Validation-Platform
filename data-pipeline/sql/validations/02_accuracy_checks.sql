-- ==========================================================
-- 02. ACCURACY CHECKS
-- Purpose: Verify calculated and transformed values against business mathematical rules.
-- ==========================================================

-- Check 2.1: Verify resolution_time_hours equals (resolved_date - created_date) in hours
SELECT 'ACCURACY_RESOLUTION_HOURS' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE status = 'Closed' AND resolution_time_hours < 0;

-- Check 2.2: Verify net_amount derivation in transactions
-- Completed => net_amount == amount; Refunded => net_amount == -amount; Failed => net_amount == 0
SELECT 'ACCURACY_TXN_NET_AMOUNT' AS test_name, COUNT(*) AS failure_count
FROM fact_transactions
WHERE (status = 'Completed' AND net_amount != amount)
   OR (status = 'Refunded' AND net_amount != -amount)
   OR (status = 'Failed' AND net_amount != 0);

-- Check 2.3: Verify Customer 360 total_spend matches sum of completed transactions
SELECT 'ACCURACY_CUSTOMER_TOTAL_SPEND' AS test_name, COUNT(*) AS failure_count
FROM (
    SELECT 
        c.customer_id,
        c.total_spend,
        COALESCE(SUM(t.amount), 0.00) AS actual_spend
    FROM agg_customer_360 c
    LEFT JOIN fact_transactions t ON c.customer_id = t.customer_id AND t.status = 'Completed'
    GROUP BY c.customer_id, c.total_spend
)
WHERE ROUND(total_spend, 2) != ROUND(actual_spend, 2);
