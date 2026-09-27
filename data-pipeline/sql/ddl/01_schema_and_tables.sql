-- DDL: Enterprise Analytics Database Schema
-- Defines relational tables for transformed silver and gold analytical layers.

-- Dimension Table: Customers
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL CHECK (tier IN ('Platinum', 'Gold', 'Silver', 'Bronze')),
    region VARCHAR(50) NOT NULL,
    account_created_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Active', 'Inactive'))
);

-- Fact Table: Service Requests
CREATE TABLE IF NOT EXISTS fact_service_requests (
    request_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (category IN ('Billing', 'Technical', 'Account', 'General')),
    priority VARCHAR(50) NOT NULL CHECK (priority IN ('Urgent', 'High', 'Medium', 'Low')),
    created_date TIMESTAMP NOT NULL,
    resolved_date TIMESTAMP NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Open', 'In_Progress', 'Closed')),
    resolution_time_hours FLOAT NULL,
    sla_compliance VARCHAR(50) NULL CHECK (sla_compliance IN ('Compliant', 'Breached') OR sla_compliance IS NULL),
    satisfaction_score FLOAT NULL CHECK (satisfaction_score BETWEEN 1 AND 5 OR satisfaction_score IS NULL),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- Fact Table: Transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    transaction_date TIMESTAMP NOT NULL,
    amount DECIMAL(18, 2) NOT NULL CHECK (amount >= 0),
    net_amount DECIMAL(18, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Completed', 'Failed', 'Refunded')),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id)
);

-- Aggregate Gold Table: Customer 360
CREATE TABLE IF NOT EXISTS agg_customer_360 (
    customer_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    tier VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    total_spend DECIMAL(18, 2) DEFAULT 0.00,
    completed_transactions_count INT DEFAULT 0,
    total_transactions_count INT DEFAULT 0,
    total_service_requests INT DEFAULT 0,
    open_service_requests INT DEFAULT 0,
    closed_service_requests INT DEFAULT 0,
    avg_satisfaction_score FLOAT NULL
);

-- Aggregate Gold Table: Category Summary
CREATE TABLE IF NOT EXISTS agg_category_summary (
    category VARCHAR(50) PRIMARY KEY,
    total_requests INT DEFAULT 0,
    closed_requests INT DEFAULT 0,
    open_requests INT DEFAULT 0,
    avg_resolution_hours FLOAT NULL,
    avg_csat FLOAT NULL
);

-- Aggregate Gold Table: Financial Daily
CREATE TABLE IF NOT EXISTS agg_financial_daily (
    tx_date DATE PRIMARY KEY,
    total_transactions INT DEFAULT 0,
    gross_volume DECIMAL(18, 2) DEFAULT 0.00,
    net_revenue DECIMAL(18, 2) DEFAULT 0.00,
    completed_transactions INT DEFAULT 0,
    failed_transactions INT DEFAULT 0,
    refunded_transactions INT DEFAULT 0
);
