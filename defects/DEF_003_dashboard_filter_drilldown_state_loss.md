# Defect Report: DEF-003

- **Defect ID:** DEF-003
- **Summary:** Dashboard filter reset and lost state when activating customer drill-down
- **Component:** Web Portal UI / Dashboard DOM
- **Severity:** Medium
- **Priority:** Medium
- **Status:** Closed
- **Assigned To:** Frontend UI Developer
- **Reported By:** Quality Engineer

---

### Description
In the web dashboard, clicking the `Drill-Down` action button on a customer record caused existing dropdown filters (e.g. Region or Tier) to be erased rather than narrowing down the current view.

### Steps to Reproduce
1. Navigate to `dashboard.html`.
2. Select `Region = 'West'`.
3. Click `Drill-Down` on customer `CUST-1002`.
4. Observe filter controls and customer list.

### Expected Result
The drill-down badge displays active customer context while preserving active region filtering.

### Actual Result
Filter dropdown was overwritten and previous state lost.

### Root Cause & Fix
Refactored `drillDownCustomer` in `app.js` to preserve active filter parameters in query state.

### Retest Result
**PASS** — Verified with Selenium test `TC-UI-06`.
