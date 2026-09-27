# Test Cases: REST API Automation (Java + REST Assured)

| Test Case ID | Endpoint | Method | Test Description | Expected Status | Expected Response Body | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-API-01** | `/api/customers` | GET | Retrieve all customer records | `200 OK` | `count >= 12`, valid customer list | **PASS** |
| **TC-API-02** | `/api/customers/:id` | GET | Retrieve existing customer `CUST-1001` | `200 OK` | `first_name: "Alice"`, `tier: "Platinum"` | **PASS** |
| **TC-API-03** | `/api/customers/:id` | GET | Query non-existent ID `CUST-9999` | `404 Not Found` | `error: "Not Found"` | **PASS** |
| **TC-API-04** | `/api/customers` | POST | Create valid customer with bearer token | `201 Created` | `message: "Customer created successfully"` | **PASS** |
| **TC-API-05** | `/api/customers` | POST | Validate rejection of invalid Tier `DiamondVIP` | `400 Bad Request` | `message: "Invalid tier..."` | **PASS** |
| **TC-API-06** | `/api/customers` | POST | Validate rejection on missing mandatory fields | `400 Bad Request` | `error: "Bad Request"` | **PASS** |
| **TC-API-07** | `/api/service-requests` | GET | Filter service requests by category `Billing` | `200 OK` | Array where all categories are `Billing` | **PASS** |
| **TC-API-08** | `/api/service-requests` | POST | Create valid service request | `201 Created` | `status: "Open"`, request created | **PASS** |
| **TC-API-09** | `/api/service-requests` | POST | Validate rejection of invalid Priority | `400 Bad Request` | `message: "Invalid priority..."` | **PASS** |
| **TC-API-10** | `/api/service-requests/:id/resolve` | PUT | Resolve ticket with valid CSAT (5) | `200 OK` | `message: "...marked as Closed"` | **PASS** |
| **TC-API-11** | `/api/service-requests/:id/resolve` | PUT | Boundary test: Reject CSAT score > 5 | `400 Bad Request` | `message: "Satisfaction score must be..."` | **PASS** |
| **TC-API-12** | `/api/metrics` | GET | Validate executive KPI totals | `200 OK` | JSON with gross volume, open/closed counts | **PASS** |
| **TC-API-13** | `/api/auth/login` | POST | Valid credentials generate auth token | `200 OK` | `token` string and `role: "Admin"` | **PASS** |
| **TC-API-14** | `/api/auth/login` | POST | Invalid credentials rejection | `401 Unauthorized` | `error: "Unauthorized"` | **PASS** |
| **TC-API-15** | `/api/customers` | POST | Missing auth header on protected endpoint | `401 Unauthorized` | `error: "Unauthorized"` | **PASS** |
| **TC-API-16** | `/api/customers` | POST | Invalid bearer token rejection | `403 Forbidden` | `error: "Forbidden"` | **PASS** |
| **TC-API-17** | End-to-End | E2E | Auth -> Create Customer -> File SR -> Resolve -> Metrics | `200/201` | Full business transaction lifecycle | **PASS** |
