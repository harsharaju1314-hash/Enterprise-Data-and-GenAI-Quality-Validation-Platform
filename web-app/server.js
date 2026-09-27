const express = require('express');
const cors = require('cors');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Database connection
const dbPath = path.join(__dirname, '..', 'data-pipeline', 'enterprise_analytics.db');
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Failed to open database:', err.message);
  } else {
    console.log('[OK] Connected to Enterprise Analytics SQLite database.');
  }
});

// Mock user tokens
const TOKENS = {
  'admin-token-12345': { username: 'admin', role: 'Admin' },
  'analyst-token-67890': { username: 'analyst', role: 'Analyst' },
  'support-token-54321': { username: 'agent', role: 'Support' }
};

// Auth Middleware
function authenticate(req, res, next) {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    return res.status(401).json({ error: 'Unauthorized', message: 'Missing Authorization header' });
  }
  const token = authHeader.replace('Bearer ', '').trim();
  if (TOKENS[token]) {
    req.user = TOKENS[token];
    next();
  } else {
    return res.status(403).json({ error: 'Forbidden', message: 'Invalid or expired auth token' });
  }
}

// ----------------------------------------------------
// 1. Authentication Endpoints
// ----------------------------------------------------
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.status(400).json({ error: 'Bad Request', message: 'Username and password are required' });
  }
  if (username === 'admin' && password === 'Admin@123') {
    return res.json({ token: 'admin-token-12345', username: 'admin', role: 'Admin' });
  } else if (username === 'analyst' && password === 'Analyst@123') {
    return res.json({ token: 'analyst-token-67890', username: 'analyst', role: 'Analyst' });
  } else if (username === 'agent' && password === 'Agent@123') {
    return res.json({ token: 'support-token-54321', username: 'agent', role: 'Support' });
  } else {
    return res.status(401).json({ error: 'Unauthorized', message: 'Invalid credentials provided' });
  }
});

// ----------------------------------------------------
// 2. Customers Endpoints
// ----------------------------------------------------
app.get('/api/customers', (req, res) => {
  const { tier, region, status } = req.query;
  let sql = 'SELECT * FROM dim_customers WHERE 1=1';
  const params = [];

  if (tier) {
    sql += ' AND tier = ?';
    params.push(tier);
  }
  if (region) {
    sql += ' AND region = ?';
    params.push(region);
  }
  if (status) {
    sql += ' AND status = ?';
    params.push(status);
  }

  db.all(sql, params, (err, rows) => {
    if (err) return res.status(500).json({ error: 'Database error', message: err.message });
    res.json({ count: rows.length, data: rows });
  });
});

app.get('/api/customers/:id', (req, res) => {
  const id = req.params.id;
  db.get('SELECT * FROM dim_customers WHERE customer_id = ?', [id], (err, row) => {
    if (err) return res.status(500).json({ error: 'Database error', message: err.message });
    if (!row) return res.status(404).json({ error: 'Not Found', message: `Customer ${id} not found` });
    res.json(row);
  });
});

app.post('/api/customers', authenticate, (req, res) => {
  const { customer_id, first_name, last_name, email, tier, region, account_created_date, status } = req.body;
  if (!customer_id || !first_name || !last_name || !email || !tier || !region) {
    return res.status(400).json({ error: 'Bad Request', message: 'Missing mandatory customer fields' });
  }

  const validTiers = ['Platinum', 'Gold', 'Silver', 'Bronze'];
  if (!validTiers.includes(tier)) {
    return res.status(400).json({ error: 'Bad Request', message: `Invalid tier. Allowed: ${validTiers.join(', ')}` });
  }

  const fullName = `${first_name.trim()} ${last_name.trim()}`;
  const createdDate = account_created_date || new Date().toISOString().split('T')[0];
  const custStatus = status || 'Active';

  const sql = `INSERT INTO dim_customers (customer_id, first_name, last_name, full_name, email, tier, region, account_created_date, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`;
  db.run(sql, [customer_id, first_name, last_name, fullName, email, tier, region, createdDate, custStatus], function (err) {
    if (err) {
      if (err.message.includes('UNIQUE') || err.message.includes('PRIMARY')) {
        return res.status(409).json({ error: 'Conflict', message: `Customer ID ${customer_id} already exists` });
      }
      return res.status(500).json({ error: 'Database error', message: err.message });
    }
    res.status(201).json({ message: 'Customer created successfully', customer_id, full_name: fullName });
  });
});

// ----------------------------------------------------
// 3. Service Requests Endpoints
// ----------------------------------------------------
app.get('/api/service-requests', (req, res) => {
  const { category, priority, status } = req.query;
  let sql = 'SELECT * FROM fact_service_requests WHERE 1=1';
  const params = [];

  if (category) {
    sql += ' AND category = ?';
    params.push(category);
  }
  if (priority) {
    sql += ' AND priority = ?';
    params.push(priority);
  }
  if (status) {
    sql += ' AND status = ?';
    params.push(status);
  }

  db.all(sql, params, (err, rows) => {
    if (err) return res.status(500).json({ error: 'Database error', message: err.message });
    res.json({ count: rows.length, data: rows });
  });
});

app.post('/api/service-requests', authenticate, (req, res) => {
  const { request_id, customer_id, category, priority, description } = req.body;
  if (!request_id || !customer_id || !category || !priority) {
    return res.status(400).json({ error: 'Bad Request', message: 'Missing mandatory service request fields' });
  }

  const validCategories = ['Billing', 'Technical', 'Account', 'General'];
  const validPriorities = ['Urgent', 'High', 'Medium', 'Low'];

  if (!validCategories.includes(category)) {
    return res.status(400).json({ error: 'Bad Request', message: `Invalid category: ${category}` });
  }
  if (!validPriorities.includes(priority)) {
    return res.status(400).json({ error: 'Bad Request', message: `Invalid priority: ${priority}` });
  }

  const createdDate = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const status = 'Open';

  const sql = `INSERT INTO fact_service_requests (request_id, customer_id, category, priority, created_date, status)
               VALUES (?, ?, ?, ?, ?, ?)`;
  db.run(sql, [request_id, customer_id, category, priority, createdDate, status], function (err) {
    if (err) {
      if (err.message.includes('UNIQUE') || err.message.includes('PRIMARY')) {
        return res.status(409).json({ error: 'Conflict', message: `Request ID ${request_id} already exists` });
      }
      return res.status(500).json({ error: 'Database error', message: err.message });
    }
    res.status(201).json({ message: 'Service request created successfully', request_id, status });
  });
});

app.put('/api/service-requests/:id/resolve', authenticate, (req, res) => {
  const id = req.params.id;
  const { satisfaction_score } = req.body;

  if (satisfaction_score !== undefined && (satisfaction_score < 1 || satisfaction_score > 5)) {
    return res.status(400).json({ error: 'Bad Request', message: 'Satisfaction score must be between 1 and 5' });
  }

  const resolvedDate = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const sql = `UPDATE fact_service_requests 
               SET status = 'Closed', resolved_date = ?, satisfaction_score = ?
               WHERE request_id = ?`;
  db.run(sql, [resolvedDate, satisfaction_score || 5, id], function (err) {
    if (err) return res.status(500).json({ error: 'Database error', message: err.message });
    if (this.changes === 0) return res.status(404).json({ error: 'Not Found', message: `Request ID ${id} not found` });
    res.json({ message: `Service request ${id} marked as Closed`, resolved_date: resolvedDate });
  });
});

// ----------------------------------------------------
// 4. Analytics & Metrics Endpoints
// ----------------------------------------------------
app.get('/api/metrics', (req, res) => {
  const sql = `
    SELECT 
      (SELECT COUNT(*) FROM fact_transactions) AS total_transactions,
      (SELECT ROUND(SUM(amount), 2) FROM fact_transactions) AS gross_transaction_volume,
      (SELECT ROUND(SUM(net_amount), 2) FROM fact_transactions) AS net_transaction_volume,
      (SELECT COUNT(*) FROM fact_service_requests) AS total_service_requests,
      (SELECT COUNT(*) FROM fact_service_requests WHERE status IN ('Open', 'In_Progress')) AS open_service_requests,
      (SELECT COUNT(*) FROM fact_service_requests WHERE status = 'Closed') AS closed_service_requests,
      (SELECT ROUND(AVG(satisfaction_score), 2) FROM fact_service_requests) AS avg_csat
  `;
  db.get(sql, [], (err, row) => {
    if (err) return res.status(500).json({ error: 'Database error', message: err.message });
    res.json(row);
  });
});

// ----------------------------------------------------
// 5. RAG Knowledge Assistant Query Endpoint
// ----------------------------------------------------
app.post('/api/rag/query', (req, res) => {
  const { question } = req.body;
  if (!question || typeof question !== 'string' || question.trim().length === 0) {
    return res.status(400).json({ error: 'Bad Request', message: 'Question parameter is required' });
  }

  const q = question.toLowerCase();

  // Guardrail check 1: Prompt Injection / System override
  if (q.includes('ignore all previous') || q.includes('system prompt') || q.includes('jailbreak') || q.includes('override instructions')) {
    return res.json({
      question,
      answer: "I am unable to process this instruction. I operate strictly within enterprise policy guidelines.",
      source_document: "Guardrail Security Filter",
      confidence: 0.0,
      guardrail_triggered: true,
      status: "GUARDRAIL_BLOCKED"
    });
  }

  // Guardrail check 2: Restricted information / PII / DB schema dump
  if (q.includes('drop table') || q.includes('password') || q.includes('credit card numbers') || q.includes('dump all database')) {
    return res.json({
      question,
      answer: "Access Denied: Inquiries regarding direct database schemas, raw security credentials, or plain text PII are restricted by the Enterprise Data Access Policy.",
      source_document: "Data Access Policy.md",
      confidence: 0.0,
      guardrail_triggered: true,
      status: "GUARDRAIL_BLOCKED"
    });
  }

  // Knowledge Retrieval Simulation from Approved Policy Documents
  if (q.includes('refund') || q.includes('money back') || q.includes('billing dispute')) {
    return res.json({
      question,
      answer: "Under the Enterprise Refund Policy, full refunds are available within 30 days of purchase if service uptime falls below 99.5%. Frontline specialists can issue credits up to $100, team leads up to $1,000, and director sign-off is required for amounts exceeding $1,000.",
      source_document: "Refund Policy.md",
      evidence: "Refund Policy Section 2: Eligibility Criteria; Section 3: Approval Matrix ($100 Specialist, $1,000 Team Lead, >$1,000 Director)",
      confidence: 0.98,
      guardrail_triggered: false,
      status: "SUCCESS"
    });
  } else if (q.includes('priority') || q.includes('urgent') || q.includes('escalat') || q.includes('sla')) {
    return res.json({
      question,
      answer: "Per the Escalation Policy, Urgent (P1) issues target resolution within 4 hours, High (P2) within 12 hours, Medium (P3) within 48 hours, and Low (P4) within 5 business days. Tickets are escalated to Tier 2 if unresolved after 50% of SLA time.",
      source_document: "Escalation Policy.md",
      evidence: "Escalation Policy Section 2: Priority Definitions & SLAs (Urgent: 4h, High: 12h, Medium: 48h, Low: 5 days)",
      confidence: 0.96,
      guardrail_triggered: false,
      status: "SUCCESS"
    });
  } else if (q.includes('support') || q.includes('hour') || q.includes('platinum') || q.includes('channel') || q.includes('csat')) {
    return res.json({
      question,
      answer: "Standard support is available Mon-Fri 8 AM to 8 PM EST via email and web portal. Platinum tier customers receive 24/7/365 priority support with a 1-hour initial response SLA and a dedicated CSM. CSAT scores below 3 trigger automated supervisor review.",
      source_document: "Customer Support Policy.md",
      evidence: "Customer Support Policy Section 2 & Section 3: Platinum 24/7/365, 1h SLA, Dedicated CSM",
      confidence: 0.97,
      guardrail_triggered: false,
      status: "SUCCESS"
    });
  } else if (q.includes('service request') || q.includes('category') || q.includes('mandatory field') || q.includes('reopen') || q.includes('re-open')) {
    return res.json({
      question,
      answer: "Service requests are categorized as Billing, Technical, Account, or General. Required fields include customer_id, category, priority, and description. Tickets can be re-opened within 14 calendar days of closure.",
      source_document: "Service Request Policy.md",
      evidence: "Service Request Policy Section 2: 4 categories; Section 3: Mandatory Fields; Section 4: 14-day re-opening window",
      confidence: 0.95,
      guardrail_triggered: false,
      status: "SUCCESS"
    });
  } else if (q.includes('access') || q.includes('rbac') || q.includes('role') || q.includes('pii')) {
    return res.json({
      question,
      answer: "The Data Access Policy defines RBAC roles: Admin (full pipeline access), Analyst (read-only silver/gold & dashboards), Support Agent (service requests & RAG), and Customer (own tickets only). PII must never be stored in plain text.",
      source_document: "Data Access Policy.md",
      evidence: "Data Access Policy Section 2: RBAC Matrix; Section 3: Sensitive Data Handling",
      confidence: 0.94,
      guardrail_triggered: false,
      status: "SUCCESS"
    });
  } else {
    // Hallucination Prevention / Missing Context Fallback
    return res.json({
      question,
      answer: "I do not have sufficient information in the approved enterprise policy documents to answer this inquiry. Please consult your administrator or support supervisor.",
      source_document: "NONE",
      confidence: 0.0,
      guardrail_triggered: false,
      status: "NO_CONTEXT_FOUND"
    });
  }
});

// Start Server
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`[OK] Enterprise Data & GenAI Server running on http://localhost:${PORT}`);
  });
}

module.exports = app;
