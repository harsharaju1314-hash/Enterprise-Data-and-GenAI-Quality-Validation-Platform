# Test Cases: UI Automation (Selenium + TypeScript)

| Test Case ID | Test Title | Page | Test Action | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-UI-01** | Invalid Login Error Banner | Login Page | Submit invalid username/password | Error banner displayed: "Invalid username or password" | **PASS** |
| **TC-UI-02** | Valid Login Authentication | Login Page | Submit valid admin credentials | Successful redirect to `dashboard.html` | **PASS** |
| **TC-UI-03** | Dashboard Initial Load & KPIs | Dashboard | Verify KPI metrics grid | Displays Gross Volume (\$5,049.74), Txns (16), CSAT (4.11) | **PASS** |
| **TC-UI-04** | Dynamic Tier Filter Application | Dashboard | Filter by Tier: `Platinum` | Table updates to show only Platinum records | **PASS** |
| **TC-UI-05** | Global Customer Search | Dashboard | Search for `CUST-1001` | Table filters to single row for Alice Smith | **PASS** |
| **TC-UI-06** | Customer Record Drilldown | Dashboard | Click `Drill-Down` on customer row | Activates drill-down state badge and filters record | **PASS** |
| **TC-UI-07** | Empty Search / Filter State | Dashboard | Filter `Tier = Platinum` & `Region = North` | Renders "No matching records found" message | **PASS** |
| **TC-UI-08** | RBAC Role Badge Display | Dashboard | Verify role chip in sidebar | Shows "Admin" role with platinum styling | **PASS** |
| **TC-UI-09** | Dashboard Data Refresh | Dashboard | Click `Refresh Data` button | Re-fetches records without page reload or errors | **PASS** |
| **TC-UI-10** | User Logout Flow | Dashboard | Click `Sign Out` button | Clears session storage and redirects to `index.html` | **PASS** |
