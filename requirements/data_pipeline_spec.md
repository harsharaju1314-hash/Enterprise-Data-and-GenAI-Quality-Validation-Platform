# Cloud Data Pipeline & ETL Quality Specification

## 1. Architecture Flow
```text
Azure Blob Storage (Raw CSVs)
       ↓
Azure Data Factory (Orchestrator)
       ↓
Azure Databricks (PySpark Bronze -> Silver -> Gold Transformations)
       ↓
Azure SQL Database (Relational Dimensional Schema)
       ↓
Qlik Sense / Web Portal (Analytics Consumption Layer)
```

## 2. Ingestion & Transformation Rules
1. **Bronze Layer (Raw Ingestion)**:
   - File formats: Delimited UTF-8 CSV (`customers.csv`, `service_requests.csv`, `transactions.csv`).
   - Schema enforcement: Required column presence and basic character validations.
2. **Silver Layer (Cleaning & Enrichment)**:
   - Primary key deduplication: `customer_id`, `request_id`, `transaction_id`.
   - String normalization: Trimming, case normalization on emails, full name derivation.
   - Categorical validation: Restricting values to predefined business enumerations.
   - Chronological validation: Ensuring `resolved_date >= created_date`.
   - Derived field calculations: `resolution_time_hours`, SLA compliance status, and net transaction amounts.
3. **Gold Layer (Business Aggregations)**:
   - Customer 360 KPIs: Total spend, transaction counts, open vs closed ticket counts, average CSAT.
   - Category Performance: Resolution rates, average resolution time, SLA compliance percentage.
   - Financial Daily Aggregates: Daily gross volume, net revenue, completion vs failure rates.

## 3. Data Quality Dimensions
- **Completeness**: No missing mandatory fields or orphaned child records.
- **Accuracy**: Calculations mathematically reconcile with raw source figures.
- **Consistency**: Primary key and foreign key referential integrity maintained across all layers.
- **Uniqueness**: Zero duplicate identifiers across tables.
- **Validity**: Enums and domain ranges match agreed standards.
- **Timeliness**: Ingested timestamps fall within valid business operational windows.
- **Source-to-Target Reconciliation**: 100% record and volume reconciliation between raw CSVs and target tables.
