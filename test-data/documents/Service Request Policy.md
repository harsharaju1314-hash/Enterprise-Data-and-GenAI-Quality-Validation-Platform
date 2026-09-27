# Service Request Policy

## 1. Purpose
This policy establishes standardized criteria for filing, categorizing, prioritizing, and managing customer service requests.

## 2. Request Categories
All service requests must be classified into one of four standard categories:
1. **Billing**: Invoices, payment processing, rate inquiries, tax certificates, and refund applications.
2. **Technical**: System bugs, API integration faults, connectivity errors, and unexpected application exceptions.
3. **Account**: User provisioning, role adjustments, password resets, contact info updates, and company profile changes.
4. **General**: Feature suggestions, documentation requests, feedback, and general advisory questions.

## 3. Mandatory Request Fields
A valid service request submission must contain:
- `customer_id`: Valid enterprise customer identifier (Format: `CUST-XXXX`).
- `category`: Must match one of [Billing, Technical, Account, General].
- `priority`: Must match one of [Urgent, High, Medium, Low].
- `title` & `description`: Minimum 10 characters explaining the inquiry.

## 4. Closure & Re-opening Guidelines
- A request is moved to `Closed` status after customer acceptance or 5 days of inactivity following a `Resolved` notification.
- Customers may re-open a closed ticket within 14 calendar days if the original issue recurs. After 14 days, a new ticket must be created referencing the previous `request_id`.
