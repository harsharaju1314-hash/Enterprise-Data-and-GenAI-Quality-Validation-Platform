-- ==========================================================
-- QLIK SENSE DASHBOARD SQL RECONCILIATION
-- Purpose: Independent SQL queries to verify every KPI and chart in Qlik Sense dashboard.
-- ==========================================================

-- KPI 1: Total Completed Transactions & Total Amount
SELECT 
    COUNT(*) AS kpi_total_transactions,
    ROUND(SUM(amount), 2) AS kpi_gross_transaction_volume,
    ROUND(SUM(net_amount), 2) AS kpi_net_transaction_volume
FROM fact_transactions;

-- KPI 2: Service Request Status Breakdown (Open vs Closed)
SELECT 
    COUNT(*) AS kpi_total_requests,
    SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) AS kpi_closed_requests,
    SUM(CASE WHEN status IN ('Open', 'In_Progress') THEN 1 ELSE 0 END) AS kpi_open_requests,
    ROUND(AVG(satisfaction_score), 2) AS kpi_avg_csat
FROM fact_service_requests;

-- Chart 1: Service Requests by Category
SELECT 
    category,
    COUNT(*) AS request_count,
    SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) AS closed_count,
    ROUND(AVG(resolution_time_hours), 2) AS avg_resolution_hours
FROM fact_service_requests
GROUP BY category
ORDER BY request_count DESC;

-- Chart 2: Daily Transaction Volume Trend
SELECT 
    DATE(transaction_date) AS txn_date,
    COUNT(*) AS total_daily_txns,
    ROUND(SUM(amount), 2) AS daily_gross_volume
FROM fact_transactions
GROUP BY DATE(transaction_date)
ORDER BY txn_date ASC;

-- Chart 3: Customer Tier Performance Metrics
SELECT 
    c.tier,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    ROUND(SUM(t.amount), 2) AS total_tier_spend,
    COUNT(sr.request_id) AS total_tier_service_requests
FROM dim_customers c
LEFT JOIN fact_transactions t ON c.customer_id = t.customer_id AND t.status = 'Completed'
LEFT JOIN fact_service_requests sr ON c.customer_id = sr.customer_id
GROUP BY c.tier
ORDER BY total_tier_spend DESC;
