# Defect Report: DEF-004

- **Defect ID:** DEF-004
- **Summary:** REST API accepted CSAT satisfaction score of 9 violating 1-5 boundary range
- **Component:** REST API / Express Validation
- **Severity:** Medium
- **Priority:** High
- **Status:** Closed
- **Assigned To:** Backend API Developer
- **Reported By:** Quality Engineer

---

### Description
During automated boundary testing (`TC-API-11`), a PUT request to `/api/service-requests/:id/resolve` with `{ "satisfaction_score": 9 }` returned HTTP `200 OK` and saved the invalid score into the database.

### Steps to Reproduce
1. Send PUT request to `/api/service-requests/SR-2005/resolve` with body `{"satisfaction_score": 9}`.
2. Verify HTTP response status code.

### Expected Result
API returns `400 Bad Request` with message: "Satisfaction score must be between 1 and 5".

### Actual Result
API returned `200 OK` and updated the database record with score 9.

### Root Cause & Fix
Added explicit range boundary check in `server.js` route handler:
```javascript
if (satisfaction_score !== undefined && (satisfaction_score < 1 || satisfaction_score > 5)) {
  return res.status(400).json({ error: 'Bad Request', message: 'Satisfaction score must be between 1 and 5' });
}
```

### Retest Result
**PASS** — Re-executed Java test `testResolveServiceRequestInvalidBoundaryScore` with `400 Bad Request` confirmed.
