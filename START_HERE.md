# Start Here — Windows

This repository is an AI-assisted assessment starter. Review it, run the tests locally, make any changes under your own Git identity, deploy it, record the demo, then submit.

## 1. Backend

PowerShell:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_employees --count 10000 --seed 42
pytest --cov=employees --cov=analytics --cov-report=term-missing
python manage.py runserver
```

Backend: http://127.0.0.1:8000/api/

## 2. Frontend

Open another PowerShell:

```powershell
cd frontend
Copy-Item .env.local.example .env.local
npm install
npm run build
npm run dev
```

Frontend: http://localhost:3000

## 3. First things to review

1. `docs/REQUIREMENTS.md`
2. `docs/CLARIFICATIONS.md`
3. `docs/ARCHITECTURE.md`
4. `docs/TRADEOFFS.md`
5. `docs/AI_USAGE.md`
6. Run all tests and the Next.js production build.
7. Test salary update, filters, dashboard, and CSV import manually.

## 4. Important submission integrity note

Do not claim tests/deployment you have not personally run. Update `docs/AI_USAGE.md` with the exact AI tools you actually used. Keep your real incremental commits while reviewing, fixing, deploying, and polishing the solution.
