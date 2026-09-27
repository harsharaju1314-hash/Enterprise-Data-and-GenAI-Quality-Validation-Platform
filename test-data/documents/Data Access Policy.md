# Data Access Policy

## 1. Purpose & Compliance
This policy governs data governance, role-based access control (RBAC), and confidentiality across enterprise analytics, cloud data platforms, and AI assistants in compliance with standard security frameworks.

## 2. Role-Based Access Controls (RBAC)
- **Admin**: Full access to cloud data pipelines (ADF, Databricks, Azure SQL), user administration, audit logs, and configuration parameters.
- **Analyst**: Read-only access to silver/gold analytical tables, Qlik Sense dashboards, and data quality validation reports. No write access to raw storage or production pipelines.
- **Support Agent**: Access to customer service request records, customer tier info, and RAG knowledge assistant. No access to financial banking details or system master credentials.
- **Customer User**: Restricted view of their own service tickets and account transaction history only.

## 3. Sensitive Data Handling
- Personally Identifiable Information (PII) such as payment card details, passwords, and private tokens must NEVER be stored in plain text or ingested into general LLM prompts without masking.
- Data retention: Transaction logs are retained for 7 years; service request attachments are archived after 3 years.
- Export restrictions: Bulk export of customer records exceeding 1,000 rows requires explicit two-factor authentication and manager approval.

## 4. AI & Knowledge Assistant Boundaries
- The GenAI assistant must only access approved enterprise policy documents contained within the designated knowledge vector store.
- Direct database schema dumping or retrieval of raw customer credentials via the AI assistant is strictly prohibited and blocked by system guardrails.
