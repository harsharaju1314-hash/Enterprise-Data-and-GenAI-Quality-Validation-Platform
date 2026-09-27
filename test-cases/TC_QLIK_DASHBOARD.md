# Test Cases: Qlik Sense Dashboard Analytics

| Test Case ID | Test Title | Scope | Test Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-QLIK-01** | Gross Volume KPI Reconciliation | KPI Validation | Verify `Sum([Gross Transaction Amount])` equals SQL aggregate | Exactly \$5,049.74 displayed | **PASS** |
| **TC-QLIK-02** | Total Completed Transactions KPI | KPI Validation | Verify `Count({<[Transaction Status]={'Completed'}>} [Transaction ID])` | Exactly 14 completed transactions | **PASS** |
| **TC-QLIK-03** | Total Service Requests KPI | KPI Validation | Verify `Count([Request ID])` matches fact table | Exactly 15 total requests | **PASS** |
| **TC-QLIK-04** | Open Service Requests KPI | KPI Validation | Verify `Sum([Is Open Request])` matches Open + In_Progress | Exactly 6 open requests | **PASS** |
| **TC-QLIK-05** | Average CSAT KPI | KPI Validation | Verify `Avg([CSAT Score])` across closed requests | Exactly 4.11 / 5.0 | **PASS** |
| **TC-QLIK-06** | Tier Filter State Recalculation | Filter Testing | Apply `Customer Tier = 'Platinum'` filter | KPIs dynamically recalculate to Platinum totals | **PASS** |
| **TC-QLIK-07** | Empty Result Filter Combination | Edge Case | Apply `Region = 'North' AND Tier = 'Platinum'` | Clean empty message without calculation exception | **PASS** |
| **TC-QLIK-08** | Drilldown to Customer Details | Drilldown | Select category `Billing` and view linked customers | Table filters to customers with billing requests | **PASS** |
