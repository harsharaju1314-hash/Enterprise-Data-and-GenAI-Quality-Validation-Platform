# Qlik Sense Dashboard & Analytics Quality Engineering Specification

## 1. Overview
This specification details the analytics data model, KPI calculation logic, filter selections, drill-down paths, and SQL reconciliation queries used to test the enterprise analytics dashboard.

## 2. Dashboard KPIs & Formula Validation Matrix

| KPI ID | KPI Label | Qlik Set Analysis Expression | SQL Verification Query | Expected Value | Tolerance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-01** | Total Gross Spend | `Sum([Gross Transaction Amount])` | `SELECT ROUND(SUM(amount), 2) FROM fact_transactions;` | **\$5,049.74** | ±\$0.00 |
| **KPI-02** | Total Completed Txns | `Count({<[Transaction Status]={'Completed'}>} [Transaction ID])` | `SELECT COUNT(*) FROM fact_transactions WHERE status='Completed';` | **14** | Exact |
| **KPI-03** | Total Service Requests | `Count([Request ID])` | `SELECT COUNT(*) FROM fact_service_requests;` | **15** | Exact |
| **KPI-04** | Open Service Requests | `Sum([Is Open Request])` | `SELECT COUNT(*) FROM fact_service_requests WHERE status IN ('Open', 'In_Progress');` | **6** | Exact |
| **KPI-05** | Closed Requests | `Sum([Is Closed Request])` | `SELECT COUNT(*) FROM fact_service_requests WHERE status = 'Closed';` | **9** | Exact |
| **KPI-06** | Average CSAT | `Avg([CSAT Score])` | `SELECT ROUND(AVG(satisfaction_score), 2) FROM fact_service_requests;` | **4.11** | ±0.01 |

## 3. Dimensions & Visualizations

1. **Service Requests by Category Bar Chart**:
   - Dimension: `category` (`Billing`, `Technical`, `Account`, `General`)
   - Measure: `Count([Request ID])`
   - Verification: `SELECT category, COUNT(*) FROM fact_service_requests GROUP BY category;`
2. **Daily Financial Volume Trend**:
   - Dimension: `Date(Floor(Timestamp(transaction_date)))`
   - Measure: `Sum(amount)`
3. **Customer Tier Spend Breakdown Pie Chart**:
   - Dimension: `tier` (`Platinum`, `Gold`, `Silver`, `Bronze`)
   - Measure: `Sum(amount)`

## 4. Dashboard Test Scenarios
- **Filter State Testing**: Applying `Tier = 'Platinum'` must dynamically recalculate all 5 KPIs to Platinum-only metrics without dropping orphaned records.
- **Drill-down Testing**: Clicking category `Billing` must filter the transaction and customer lists to only customers with billing requests.
- **Empty Result Handling**: Selecting filter combination `Region = 'North' AND Tier = 'Platinum'` displays a clean "No records match current filter criteria" state without runtime error.
- **Access Control Testing**: Analyst role can view all aggregated KPIs and export summary CSV; Support Agent role has masked financial aggregates.
