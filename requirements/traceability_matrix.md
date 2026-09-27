# Requirement Traceability Matrix (RTM)

## End-to-End Quality Traceability

| Req ID | Requirement Description | Test Scenario | Test Case ID | Test Automation Layer | Status | Defect ID | Retest Result |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-01** | Cloud Data Ingestion & Transformation | Verify deduplication, cleaning, and table loading | TC-DATA-01 to TC-DATA-07 | Databricks / Python DQ Engine / SQL | **PASS** | DEF-001, DEF-002 | **PASS** |
| **BR-01** | Source-to-Target Reconciliation | Compare Blob CSV record counts & gross volume vs SQL | TC-DATA-08 to TC-DATA-10 | Python Reconciliation CLI | **PASS** | DEF-001 | **PASS** |
| **BR-02** | Qlik Sense Dashboard Calculations | Reconcile Gross Volume, Txns, CSAT against SQL | TC-QLIK-01 to TC-QLIK-06 | SQL Reconciliation Queries | **PASS** | DEF-007 | **PASS** |
| **BR-02** | Dashboard Multi-tier Filtering & Drilldown | Dynamic filtering by Tier and Customer search | TC-UI-04 to TC-UI-06 | Selenium + TypeScript | **PASS** | DEF-003 | **PASS** |
| **BR-03** | Customer & Service Request REST API | CRUD operations, pagination, query filtering | TC-API-01 to TC-API-08 | Java + REST Assured | **PASS** | - | **PASS** |
| **BR-03** | API Boundary & Negative Validation | Boundary validation on CSAT score & invalid Tiers | TC-API-09 to TC-API-11 | Java + REST Assured | **PASS** | DEF-004 | **PASS** |
| **BR-03** | Authentication & RBAC Security | Bearer token validation and 401/403 handling | TC-API-13 to TC-API-16 | Java + REST Assured | **PASS** | - | **PASS** |
| **BR-04** | Grounded Policy Retrieval & Q&A | Answering questions from approved policies | GENAI-TC-01 to GENAI-TC-07 | Python Eval Framework | **PASS** | - | **PASS** |
| **BR-04** | Hallucination Prevention | Safe refusal on non-existent policy topics | GENAI-TC-08, GENAI-TC-09 | Python Eval Framework | **PASS** | DEF-005 | **PASS** |
| **BR-04** | Prompt Variations & Consistency | Handling lexical variations and equivalent prompts | GENAI-TC-10, 11, 15 | Python Eval Framework | **PASS** | - | **PASS** |
| **BR-05** | Prompt Injection & Safety Guardrails | Intercepting jailbreaks, PII, and SQL exfiltration | GENAI-TC-12 to GENAI-TC-14 | Python Guardrails Suite | **PASS** | DEF-006 | **PASS** |
| **BR-02** | Web Portal End-to-End Regression | Full UI lifecycle: login, filter, search, drilldown, logout | TC-UI-01 to TC-UI-10 | Selenium + TypeScript | **PASS** | DEF-003 | **PASS** |
