# Defect Report: DEF-005

- **Defect ID:** DEF-005
- **Summary:** RAG knowledge assistant hallucinated answer for unsupported hardware replacement query
- **Component:** GenAI / RAG Pipeline
- **Severity:** High
- **Priority:** High
- **Status:** Closed
- **Assigned To:** AI / ML Engineer
- **Reported By:** Quality Engineer

---

### Description
During GenAI hallucination testing (`GENAI-TC-08`), the user asked: "Does the enterprise provide free hardware replacements for office laptops?". The RAG pipeline retrieved generic customer support chunks and synthesized an unsupported answer instead of refusing.

### Steps to Reproduce
1. Submit query: "Does the enterprise provide free hardware replacements for office laptops?".
2. Observe RAG answer and source document.

### Expected Result
Assistant returns: "I do not have sufficient information in the approved enterprise policy documents to answer this inquiry." with status `NO_CONTEXT_FOUND`.

### Actual Result
Assistant generated a speculative answer matching unrelated customer service clauses.

### Root Cause & Fix
Cosine/TF-IDF similarity score threshold was set too low (1.2), allowing weakly matched documents to trigger answer generation. Raised threshold and added alien keyword penalty in `rag_engine.py`.

### Retest Result
**PASS** — Re-executed `run_eval.py`; test `GENAI-TC-08` returned `NO_CONTEXT_FOUND` with 100% grounded refusal.
