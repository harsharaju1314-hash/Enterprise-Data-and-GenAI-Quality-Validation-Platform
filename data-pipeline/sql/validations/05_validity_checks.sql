-- ==========================================================
-- 05. VALIDITY CHECKS
-- Purpose: Validate allowed enumeration sets, ranges, and patterns.
-- ==========================================================

-- Check 5.1: Customer Tier Validity
SELECT 'INVALID_CUSTOMER_TIER' AS test_name, COUNT(*) AS failure_count
FROM dim_customers
WHERE tier NOT IN ('Platinum', 'Gold', 'Silver', 'Bronze');

-- Check 5.2: Service Request Category Validity
SELECT 'INVALID_SR_CATEGORY' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE category NOT IN ('Billing', 'Technical', 'Account', 'General');

-- Check 5.3: Service Request Priority Validity
SELECT 'INVALID_SR_PRIORITY' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE priority NOT IN ('Urgent', 'High', 'Medium', 'Low');

-- Check 5.4: CSAT Score Range Validity (1 to 5)
SELECT 'INVALID_CSAT_RANGE' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE satisfaction_score IS NOT NULL AND (satisfaction_score < 1 OR satisfaction_score > 5);

-- Check 5.5: Non-negative Transaction Amounts
SELECT 'INVALID_NEGATIVE_AMOUNT' AS test_name, COUNT(*) AS failure_count
FROM fact_transactions
WHERE amount < 0;
