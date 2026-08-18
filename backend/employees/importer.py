import csv
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from io import TextIOWrapper
from django.db import transaction
from .models import Employee
from .services import SUPPORTED_CURRENCIES, get_reporting_rate, normalize_to_usd

REQUIRED_COLUMNS = {
    "employee_id", "first_name", "last_name", "email", "department", "job_title",
    "job_level", "country", "currency", "annual_salary", "hire_date",
}
VALID_LEVELS = {choice[0] for choice in Employee.LEVELS}

@dataclass
class ImportResult:
    imported: int
    errors: list[dict]


def _row_error(row_number, field, message):
    return {"row": row_number, "field": field, "message": message}


def import_employee_csv(uploaded_file) -> ImportResult:
    wrapper = TextIOWrapper(uploaded_file.file, encoding="utf-8-sig", newline="")
    reader = csv.DictReader(wrapper)
    missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
    if missing:
        return ImportResult(0, [{"row": 1, "field": "header", "message": f"Missing columns: {', '.join(sorted(missing))}"}])

    employees, errors = [], []
    seen_ids, seen_emails = set(), set()
    existing_ids = set(Employee.objects.values_list("employee_id", flat=True))
    existing_emails = set(Employee.objects.values_list("email", flat=True))

    for row_number, row in enumerate(reader, start=2):
        emp_id = (row.get("employee_id") or "").strip()
        email = (row.get("email") or "").strip().lower()
        currency = (row.get("currency") or "").strip().upper()
        level = (row.get("job_level") or "").strip().upper()

        if not emp_id:
            errors.append(_row_error(row_number, "employee_id", "Required.")); continue
        if emp_id in seen_ids or emp_id in existing_ids:
            errors.append(_row_error(row_number, "employee_id", "Duplicate employee ID.")); continue
        if not email or "@" not in email:
            errors.append(_row_error(row_number, "email", "Valid email required.")); continue
        if email in seen_emails or email in existing_emails:
            errors.append(_row_error(row_number, "email", "Duplicate email.")); continue
        if currency not in SUPPORTED_CURRENCIES:
            errors.append(_row_error(row_number, "currency", "Unsupported currency.")); continue
        if level not in VALID_LEVELS:
            errors.append(_row_error(row_number, "job_level", f"Choose one of: {', '.join(sorted(VALID_LEVELS))}")); continue

        try:
            salary = Decimal((row.get("annual_salary") or "").strip())
            if salary <= 0: raise InvalidOperation
        except (InvalidOperation, ValueError):
            errors.append(_row_error(row_number, "annual_salary", "Positive numeric salary required.")); continue

        try:
            hire_date = datetime.strptime((row.get("hire_date") or "").strip(), "%Y-%m-%d").date()
        except ValueError:
            errors.append(_row_error(row_number, "hire_date", "Use YYYY-MM-DD.")); continue

        rate = get_reporting_rate(currency)
        employees.append(Employee(
            employee_id=emp_id,
            first_name=(row.get("first_name") or "").strip(),
            last_name=(row.get("last_name") or "").strip(),
            email=email,
            department=(row.get("department") or "").strip(),
            job_title=(row.get("job_title") or "").strip(),
            job_level=level,
            country=(row.get("country") or "").strip(),
            currency=currency,
            annual_salary=salary,
            exchange_rate_to_usd=rate,
            annual_salary_usd=normalize_to_usd(salary, rate),
            hire_date=hire_date,
        ))
        seen_ids.add(emp_id); seen_emails.add(email)

    if errors:
        return ImportResult(0, errors[:100])

    with transaction.atomic():
        Employee.objects.bulk_create(employees, batch_size=1000)
    return ImportResult(len(employees), [])
