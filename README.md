# ACME Compensation Manager

A focused take-home assessment implementation for Incubyte's Salary Management problem. It replaces spreadsheet-driven compensation tracking with a searchable employee directory, salary editing/history, CSV onboarding, and deterministic compensation analytics for a synthetic 10,000-person organization.

## Product highlights

- Search, filter, sort, and paginate employee compensation records server-side.
- Update compensation with an immutable salary-change audit trail.
- Import legacy spreadsheet data through CSV validation and batched inserts.
- Analyze total normalized payroll, average/median compensation, country and department breakdowns, and salary distribution.
- Seed exactly 10,000 realistic synthetic employees with deterministic output.
- Keep multi-currency reporting auditable through stored local salary, FX snapshot, and normalized USD amount.
- Backend unit/API tests cover domain validation, history, filtering, analytics, CSV import, and seeding behavior.

## Architecture

```text
Browser
  |
  v
Next.js 16 UI
  |
  | JSON / multipart CSV
  v
Django 5.2 LTS + Django REST Framework
  |
  +-- employee domain + salary history
  +-- reporting/analytics service
  +-- CSV import + seed command
  |
  v
PostgreSQL (deployment) / SQLite (zero-config local development)
```

This is intentionally a modular monolith. At 10,000 employees, microservices, queues, and distributed caches would add operational complexity without solving a demonstrated scale problem.

## Quick start (zero-config SQLite)

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_employees --count 10000
python manage.py runserver
```

API: `http://localhost:8000/api/`

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

UI: `http://localhost:3000`

## Docker development

```bash
docker compose up --build
```

Then seed the database:

```bash
docker compose exec backend python manage.py seed_employees --count 10000
```

## Useful API endpoints

```text
GET    /api/employees/
GET    /api/employees/{id}/
POST   /api/employees/
PATCH  /api/employees/{id}/
DELETE /api/employees/{id}/
POST   /api/employees/import_csv/
GET    /api/employees/{id}/salary_history/

GET    /api/analytics/summary/
GET    /api/analytics/by_department/
GET    /api/analytics/by_country/
GET    /api/analytics/salary_distribution/
```

Example filtering:

```text
/api/employees/?search=engineer&department=Engineering&country=India&salary_min=50000&ordering=-annual_salary_usd&page=1
```

## Tests

```bash
cd backend
pytest
```

Coverage is configured for the domain apps:

```bash
pytest --cov=employees --cov=analytics --cov-report=term-missing
```

## Seed determinism

`seed_employees` accepts a seed value so reviewers can reproduce the same 10,000-person dataset:

```bash
python manage.py seed_employees --count 10000 --seed 42 --reset
```

## Multi-currency decision

Adding INR, GBP, EUR, JPY, etc. directly would make total-payroll analytics incorrect. Each record therefore stores:

- local annual salary,
- local currency,
- the FX rate snapshot used for reporting,
- normalized annual salary in USD.

For the assessment, FX rates are deterministic **illustrative seed/reporting constants, not live market rates**. A real deployment would source approved finance-controlled rates and version them by effective date.

## Security boundary

The deployed assessment must contain **synthetic data only**. Enterprise authentication, SSO, fine-grained RBAC, encryption/key management policy, and approval workflows are intentionally not simulated as fake "production security". They are documented as mandatory production follow-ups in `docs/TRADEOFFS.md`.

## Assessment artifacts

- `docs/REQUIREMENTS.md` — one-page product requirements and non-goals.
- `docs/ARCHITECTURE.md` — component/data design and key decisions.
- `docs/TRADEOFFS.md` — explicit scope and engineering trade-offs.
- `docs/PERFORMANCE.md` — performance considerations for 10k employees and growth.
- `docs/AI_USAGE.md` — how AI was used, how output was verified, and example prompts.
- `docs/CLARIFICATIONS.md` — questions worth sending to the hiring team.
- `docs/DEMO_SCRIPT.md` — concise 3–5 minute walkthrough.
- `docs/COMMIT_PLAN.md` — incremental commit narrative.

## Deployment

Recommended split:

- Frontend: Vercel
- Backend: Render/Railway/Fly.io or similar container runtime
- Database: managed PostgreSQL

Set `NEXT_PUBLIC_API_URL` to the deployed backend `/api` URL and configure backend `DATABASE_URL`, `DJANGO_ALLOWED_HOSTS`, and `CORS_ALLOWED_ORIGINS`.
