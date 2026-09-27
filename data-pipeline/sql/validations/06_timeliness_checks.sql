-- ==========================================================
-- 06. TIMELINESS CHECKS
-- Purpose: Verify source data ingestion fresh timestamps and SLA processing windows.
-- ==========================================================

-- Check 6.1: Verify resolved date occurs on or after created date
SELECT 'CHRONOLOGY_VIOLATION' AS test_name, COUNT(*) AS failure_count
FROM fact_service_requests
WHERE resolved_date IS NOT NULL AND resolved_date < created_date;

-- Check 6.2: Ensure records exist for the active processing period
SELECT 'DATA_FRESHNESS_EMPTY_CHECK' AS test_name,
       CASE WHEN COUNT(*) > 0 THEN 0 ELSE 1 END AS failure_count
FROM fact_transactions
WHERE transaction_date >= '2025-08-01';
