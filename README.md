# Enterprise Data & GenAI Quality Validation Platform

## Overview
The **Enterprise Data & GenAI Quality Validation Platform** is an end-to-end quality engineering framework designed to validate cloud data pipelines, relational data warehouses, operational analytics dashboards, backend REST APIs, and Retrieval-Augmented Generation (RAG) AI applications.

The platform provides a realistic, modular test architecture covering data quality dimensions, source-to-target reconciliation, automated API test suites, UI regression automation, and multi-dimensional GenAI evaluation benchmarks.

---

## Problem Statement
Modern enterprise architectures combine cloud ETL/ELT pipelines, business intelligence dashboards, and LLM-powered knowledge assistants. Quality validation across these interconnected layers presents specific challenges:
- **Data Pipeline Integrity**: Silent data loss, schema drift, improper deduplication, or rounding errors between raw blob storage and analytical data warehouses.
- **Dashboard Metric Consistency**: Discrepancies between business intelligence KPI calculations (e.g. in Qlik Sense) and underlying relational SQL stores.
- **API Reliability & Boundaries**: Inadequate boundary validation, improper status codes, or authorization gaps in business microservices.
- **GenAI Hallucination & Security Risks**: LLMs generating ungrounded assertions on missing context, susceptibility to prompt injections, or leaking restricted data.

This project implements an automated, auditable Quality Engineering platform to systematically detect and prevent defects across each tier.

---

## Key Features
- **Cloud ETL/ELT Ingestion & Transformation**: Automated pipeline processing raw CSV datasets from Azure Blob Storage through Databricks cleaning notebooks into Azure SQL analytics tables.
- **7-Dimension SQL Data Quality Suite**: Automated verification of **Completeness**, **Accuracy**, **Consistency**, **Uniqueness**, **Validity**, **Timeliness**, and **Source-to-Target Reconciliation**.
- **Qlik Sense Analytics Validation**: QVS load script models and independent SQL reconciliation queries verifying executive KPIs, filter dynamics, and drill-down states.
- **Java REST Assured Automation**: Comprehensive API test suite testing CRUD operations, authentication, boundary ranges, negative scenarios, and end-to-end integration flows.
- **Selenium TypeScript UI Regression Suite**: Page Object Model (POM) automation covering 10 user journeys (authentication, dynamic filtering, search, drill-down, empty states, RBAC, logout).
- **Enterprise RAG Knowledge Assistant**: Retrieval-Augmented Generation pipeline leveraging approved enterprise policies with strict document citation.
- **GenAI Evaluation & Guardrails Framework**: 15 quantitative evaluation benchmarks measuring **Functional Correctness**, **Answer Relevance**, **Groundedness**, **Hallucination Prevention**, **Retrieval Accuracy**, **Prompt Variations**, **Guardrail Security**, and **Factual Consistency**.
- **Defect Management & Traceability**: Complete Requirement Traceability Matrix (RTM) linking business requirements to test cases, automation suites, and resolved defect reports.

---

## Tech Stack
- **Cloud & Data Pipeline**: Azure Blob Storage (Simulated), Azure Data Factory (JSON Pipeline Definitions), Databricks (PySpark / Python ETL), Azure SQL Database (Relational Schema & DDL)
- **Business Intelligence**: Qlik Sense (QVS Load Script & Master Items)
- **API Automation**: Java 17, REST Assured 5.4.0, JUnit 5, Jackson Databind, Maven
- **UI Automation**: TypeScript, Selenium WebDriver 4.19, Mocha, Chai, ts-node, Chrome Headless
- **GenAI & RAG**: Python 3.12, LangChain, Document Indexer, Vector TF-IDF / Cosine Retrieval, AI Safety Guardrails
- **Backend Application**: Node.js, Express, SQLite3

---

## System Architecture / Workflow

```text
+---------------------------------------------------------------------------------------+
|                               CLOUD DATA PIPELINE LAYER                               |
|                                                                                       |
|  [Azure Blob Storage] ---> [Azure Data Factory] ---> [Databricks] ---> [Azure SQL]    |
|   (Raw CSV Datasets)        (Orchestrator)            (PySpark ETL)     (Relational)  |
+---------------------------------------------------------------------------------------+
                                                                 |
                                                                 v
+---------------------------------------------------------------------------------------+
|                                APPLICATION & SERVING LAYER                            |
|                                                                                       |
|  [REST API Backend] <------------------------------------------+                      |
|   (Express Server)                                             |                      |
|          |                                                     v                      |
|          +----------> [Qlik Sense & Web Dashboard]    [RAG Knowledge Assistant]       |
|          |             (Analytics KPIs & Filters)      (Approved Policy Docs)         |
+----------|-----------------------------------------------------|----------------------+
           |                                                     |
           v                                                     v
+---------------------------------------------------------------------------------------+
|                             QUALITY ENGINEERING TEST AUTOMATION                       |
|                                                                                       |
|  * Java + REST Assured API Tests (17 Test Cases)                                      |
|  * Selenium + TypeScript UI Tests (10 POM Test Cases)                                 |
|  * 7-Dimension SQL Data Quality & Reconciliation Suite (19 Checks)                    |
|  * GenAI Evaluation Benchmark & Regression Harness (15 Multi-Dimension Checks)        |
+---------------------------------------------------------------------------------------+
```

### High-Level Request Flow
`User / Client` &rarr; `REST API / UI` &rarr; `Business Logic & Guardrails` &rarr; `Database / RAG Vector Store` &rarr; `Verified Grounded Response`

---

## Project Structure

```text
Enterprise-Data-and-GenAI-Quality-Validation-Platform/
├── README.md
├── .gitignore
├── requirements/
│   ├── business_requirements.md
│   ├── data_pipeline_spec.md
│   ├── rag_assistant_spec.md
│   └── traceability_matrix.md
├── test-plan/
│   ├── master_test_plan.md
│   └── test_strategy_cloud_and_genai.md
├── test-cases/
│   ├── TC_DATA_PIPELINE.md
│   ├── TC_QLIK_DASHBOARD.md
│   ├── TC_API_AUTOMATION.md
│   ├── TC_UI_AUTOMATION.md
│   └── TC_GENAI_RAG_EVALUATION.md
├── test-data/
│   ├── raw_blob/
│   │   ├── customers.csv
│   │   ├── service_requests.csv
│   │   └── transactions.csv
│   └── documents/
│       ├── Customer Support Policy.md
│       ├── Data Access Policy.md
│       ├── Escalation Policy.md
│       ├── Refund Policy.md
│       └── Service Request Policy.md
├── data-pipeline/
│   ├── adf/
│   │   ├── pipeline/PL_Enterprise_Data_Ingest_Transform.json
│   │   ├── linkedService/
│   │   ├── dataset/
│   │   └── trigger/TR_Daily_Batch_Scheduled.json
│   ├── databricks/
│   │   ├── 01_bronze_to_silver_cleaning.py
│   │   ├── 02_silver_to_gold_aggregates.py
│   │   └── run_databricks_etl.py
│   └── sql/
│       ├── ddl/01_schema_and_tables.sql
│       ├── validations/
│       │   ├── 01_completeness_checks.sql
│       │   ├── 02_accuracy_checks.sql
│       │   ├── 03_consistency_checks.sql
│       │   ├── 04_uniqueness_checks.sql
│       │   ├── 05_validity_checks.sql
│       │   ├── 06_timeliness_checks.sql
│       │   └── 07_source_to_target_reconciliation.sql
│       └── dashboard_reconciliation.sql
├── data-validation/
│   ├── data_quality_engine.py
│   ├── run_reconciliation.py
│   └── test_data_pipeline.py
├── qlik/
│   ├── app_load_script.qvs
│   ├── data_model_metadata.json
│   └── qlik_kpi_spec.md
├── web-app/
│   ├── package.json
│   ├── server.js
│   └── public/
│       ├── index.html
│       ├── dashboard.html
│       ├── rag_assistant.html
│       ├── styles.css
│       └── app.js
├── api-tests/
│   ├── pom.xml
│   └── src/
│       ├── main/java/com/enterprise/quality/api/
│       │   ├── config/TestConfig.java
│       │   ├── models/
│       │   └── utils/SpecBuilder.java, AuthHelper.java
│       └── test/java/com/enterprise/quality/api/
│           ├── CustomersApiTest.java
│           ├── ServiceRequestsApiTest.java
│           ├── MetricsAndAnalyticsApiTest.java
│           ├── AuthorizationAndSecurityApiTest.java
│           └── EndToEndIntegrationApiTest.java
├── ui-tests/
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── pages/BasePage.ts, LoginPage.ts, DashboardPage.ts, RagAssistantPage.ts
│       └── tests/regression.spec.ts
├── rag-application/
│   ├── rag_engine.py
│   ├── guardrails.py
│   ├── app_cli.py
│   └── requirements.txt
├── genai-evaluation/
│   ├── datasets/evaluation_benchmark_dataset.json
│   ├── eval_metrics.py
│   ├── run_eval.py
│   ├── regression_runner.py
│   └── reports/evaluation_report.md
├── defects/
│   ├── DEFECT_LOG.md
│   ├── DEF_001_source_target_rounding_discrepancy.md
│   ├── DEF_002_service_request_status_null_handling.md
│   ├── DEF_003_dashboard_filter_drilldown_state_loss.md
│   ├── DEF_004_api_boundary_negative_amount_validation.md
│   ├── DEF_005_rag_hallucination_out_of_policy_query.md
│   ├── DEF_006_prompt_injection_guardrail_bypass.md
│   └── DEF_007_qlik_sql_reconciliation_aggregate_drift.md
└── screenshots/
    └── .gitkeep
```

---

## Installation & Setup

### Prerequisites
- **Node.js**: v18+ (tested on v24)
- **Java JDK**: 17+
- **Apache Maven**: 3.9+
- **Python**: 3.10+ (tested on 3.12)
- **Google Chrome**: Installed for Selenium WebDriver

### 1. Clone the Repository
```bash
git clone https://github.com/harsharaju1314-hash/Enterprise-Data-and-GenAI-Quality-Validation-Platform.git
cd Enterprise-Data-and-GenAI-Quality-Validation-Platform
```

### 2. Install Python Dependencies
```bash
pip install pandas numpy pytest requests
```

### 3. Install Web Application & UI Test Dependencies
```bash
cd web-app
npm install
cd ../ui-tests
npm install
cd ..
```

---

## Running the Application & Tests

### Step 1: Run Databricks ETL & Generate Database
Executes bronze-to-silver cleaning, gold aggregations, and populates relational database tables:
```bash
python data-pipeline/databricks/run_databricks_etl.py
```

### Step 2: Execute Data Quality & Source-to-Target Reconciliation
Runs the 19 automated SQL validation checks across all 7 dimensions:
```bash
python data-validation/run_reconciliation.py
```

### Step 3: Start the Backend Web Server
Starts the Express REST API and web dashboard at `http://localhost:4000`:
```bash
cd web-app
npm start
```
*(Leave server running in terminal)*

### Step 4: Run Java + REST Assured API Automation
In a new terminal, execute the 17 REST Assured test cases:
```bash
cd api-tests
mvn test
```

### Step 5: Run Selenium TypeScript UI Regression Suite
Executes the 10 UI automation regression tests in Chrome headless mode:
```bash
cd ui-tests
npm test
```

### Step 6: Execute GenAI RAG Evaluation & Safety Benchmark
Evaluates the RAG assistant across 15 benchmark questions and generates a markdown report:
```bash
python genai-evaluation/run_eval.py
```

---

## REST API Endpoints

| Method | Endpoint | Purpose | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Authenticate user and issue role-based token | No |
| `GET` | `/api/customers` | Query customers with optional tier/region filters | No |
| `GET` | `/api/customers/:id` | Retrieve customer record by ID | No |
| `POST` | `/api/customers` | Create new customer record with validation | Yes (Bearer) |
| `GET` | `/api/service-requests` | Query service requests with category/status filters | No |
| `POST` | `/api/service-requests` | Submit new service request | Yes (Bearer) |
| `PUT` | `/api/service-requests/:id/resolve`| Resolve service request and capture CSAT score | Yes (Bearer) |
| `GET` | `/api/metrics` | Retrieve aggregated dashboard KPIs | No |
| `POST` | `/api/rag/query` | Submit prompt to RAG knowledge assistant | No |

---

## Database Schema & Data Quality Strategy

### Relational Schema Design
- **`dim_customers`**: Master customer records (`customer_id`, `first_name`, `last_name`, `email`, `tier`, `region`, `status`).
- **`fact_service_requests`**: Ticket lifecycles (`request_id`, `customer_id`, `category`, `priority`, `created_date`, `resolved_date`, `status`, `resolution_time_hours`, `satisfaction_score`).
- **`fact_transactions`**: Financial ledger (`transaction_id`, `customer_id`, `transaction_date`, `amount`, `net_amount`, `payment_method`, `channel`, `status`).
- **`agg_customer_360`**: Pre-aggregated customer spend, ticket volume, and satisfaction metrics.

### 7-Dimension Validation Summary
| Dimension | Check Description | Expected Result | Result |
| :--- | :--- | :--- | :--- |
| **Completeness** | Mandatory null checks on all primary keys and critical attributes | 0 Nulls | **PASS** |
| **Accuracy** | Net amount derivations and non-negative resolution durations | 100% Match | **PASS** |
| **Consistency** | Referential integrity between fact tables and customer dimension | 0 Orphans | **PASS** |
| **Uniqueness** | Primary key uniqueness across customers, requests, and transactions | 0 Duplicates | **PASS** |
| **Validity** | Enum value checks (Tiers, Categories, Priorities, CSAT 1-5) | 100% Valid | **PASS** |
| **Timeliness** | Chronological checks (`resolved_date >= created_date`) | 0 Violations | **PASS** |
| **Reconciliation** | Blob storage row count & gross amount vs SQL table | Exactly \$5,049.74 / 16 Txns | **PASS** |

---

## GenAI Evaluation Methodology

The GenAI Evaluation Framework assesses the RAG knowledge assistant across 8 specific quality criteria using structured benchmark datasets:

```text
Test Dataset (15 Prompts)
       ↓
Guardrail Inspection (Prompt Injection / PII / Scope)
       ↓
Document Retrieval (Top-k Chunks from 5 Policy Documents)
       ↓
Grounded Generation (Context-Constrained Answer)
       ↓
Multi-Dimension Evaluation Metric Engine
       ↓
Pass/Fail Determination & Detailed Markdown Report
```

### Benchmark Results (15/15 Passed - 100.0% Pass Rate)
- **Functional Correctness**: Exact policy alignment for SLA targets, refund thresholds, and mandatory fields.
- **Relevance**: Average Token F1 score of **`0.745`** against expected golden answers.
- **Groundedness**: **`0.771`** score verifying every answer is backed by approved policy evidence.
- **Retrieval Accuracy**: **`1.00 (100%)`** precision across indexed policy chunks.
- **Guardrail Precision**: **`1.00 (100%)`** interception of prompt injections and schema exfiltration.
- **Hallucination Prevention**: Explicit refusal on out-of-domain queries (e.g. laptop hardware, stock dividends).

---

## Application Screenshots (Placeholders)

![Application Screenshot](screenshots/dashboard.png)
*Figure 1: Executive Analytics Dashboard with Qlik Sense Verified KPIs and Filter Controls*

![AI Knowledge Assistant](screenshots/rag_assistant.png)
*Figure 2: Grounded RAG Assistant Interface with Policy Citations and Guardrail Feedback*

---

## Defect Management Summary
Seven realistic defects were documented, investigated, resolved, and retested:
- **DEF-001**: Databricks transaction net amount floating-point rounding drift (Closed - Verified).
- **DEF-002**: Closed service requests persisted with NULL resolved date (Closed - Verified).
- **DEF-003**: Web UI filter state cleared upon customer drill-down action (Closed - Verified).
- **DEF-004**: REST API accepted out-of-bounds CSAT scores > 5 (Closed - Verified).
- **DEF-005**: RAG assistant hallucinated speculative answer on unsupported laptop policy (Closed - Verified).
- **DEF-006**: Prompt injection bypassed naive string filter via lowercase jailbreak (Closed - Verified).
- **DEF-007**: Qlik Sense KPI calculation excluded refunded amounts from net metrics (Closed - Verified).

---

## What I Learned / Key Takeaways
1. **Multi-Stage Data Validation**: Implementing source-to-target reconciliation at each pipeline hop prevents silent data corruption that single-point assertions miss.
2. **Deterministic vs Evaluative Testing**: Traditional software testing relies on binary assertions ($f(x) = y$), whereas GenAI applications require multi-dimensional scoring (relevance, groundedness, guardrails, retrieval precision).
3. **Defense-in-Depth for AI Systems**: Grounding LLMs with strict context thresholds and layered regex/semantic guardrails prevents hallucinations and prompt injection vulnerabilities.
4. **End-to-End Quality Traceability**: Maintaining a structured RTM connecting requirements to API, UI, SQL, and GenAI test cases ensures complete quality visibility for audits and releases.

---

## Future Improvements
- Integrate Azure Key Vault linked services for runtime secrets rotation.
- Extend REST Assured test suite with automated OpenAPI schema contract tests.
- Integrate ChromaDB / FAISS vector database container for high-concurrency policy document search.
- Configure GitHub Actions CI workflow to trigger full regression test gates on pull requests.

---

## Author
**Harsha Raju**  
Quality Engineer | Cloud Data, Test Automation & GenAI Quality  
GitHub: [harsharaju1314-hash](https://github.com/harsharaju1314-hash)
