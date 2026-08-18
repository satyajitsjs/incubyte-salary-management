# Product Requirements — ACME Compensation Manager

## Goal and success criteria
ACME HR currently manages compensation for ~10,000 employees across multiple countries in spreadsheets. The MVP should give an HR Manager one trustworthy web workspace to locate employee salary data, maintain it, migrate existing spreadsheet records, and answer common organization-level compensation questions. Success means common lookups/updates take seconds, reporting is deterministic and explainable, and no workflow requires loading all 10,000 records into the browser.

## Primary user
**HR Manager** — responsible for maintaining employee compensation records and answering internal compensation/payroll questions.

## Core jobs to be done
1. Find an employee or cohort quickly by name, ID, department, country, role, and salary range.
2. View and edit an employee's current annual salary without losing the previous value.
3. Understand overall payroll and compensation patterns: total normalized payroll, average/median salary, distribution, department breakdown, and country breakdown.
4. Migrate existing spreadsheet data through CSV import with clear validation errors.
5. Exportability is desirable, but data correctness and migration-in are higher priority for the MVP.

## MVP scope / features
- Employee directory with server-side pagination, search, filters, and sorting.
- Employee detail view with current compensation and salary-change history.
- Create/update/delete employee records with domain validation.
- Multi-country/multi-currency storage with an explicit FX snapshot and normalized USD reporting salary so cross-country aggregates are mathematically meaningful.
- Compensation dashboard with deterministic aggregate metrics and breakdowns.
- CSV import for existing Excel-exported data; reject malformed/duplicate rows rather than silently corrupting data.
- Deterministic seed command for exactly 10,000 synthetic employees.
- Responsive web UI, backend API, relational database, automated tests, Docker/local setup, and deployable configuration.

## Deliberate non-goals
- **Payroll execution, taxes, payslips, banking:** materially different regulated domain; not required to solve salary-data management.
- **Employee self-service / manager workflows:** persona is HR Manager; adds permissions and workflow scope before core HR needs are validated.
- **SSO, enterprise RBAC, approval workflows:** mandatory before real salary data goes live, but fake authentication in a take-home adds little evidence of product value. Assessment deployment must use synthetic data only.
- **Live FX conversion:** finance teams normally control approved reporting rates. MVP stores an auditable rate snapshot and deterministic constants; production should integrate versioned, approved rates.
- **LLM salary chatbot / recommendations:** deterministic analytics meet the stated questions more reliably and avoid privacy, hallucination, auditability, and cost concerns. Add natural-language querying only if explicitly required.
- **Microservices, queues, Redis/Kafka:** unnecessary for 10,000 employee records; a modular monolith is simpler to operate and test.

## Acceptance criteria
- 10,000 seeded employees can be browsed without client-side full-dataset loading.
- Search/filter/sort/pagination work together and return stable results.
- Negative/zero salary and unsupported currency values are rejected.
- Salary changes create an audit-history record.
- Dashboard totals use normalized reporting salary rather than summing mixed currencies.
- CSV import returns understandable row-level errors and performs no partial import on validation failure.
- Core unit/API tests are fast and deterministic.
