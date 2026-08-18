from datetime import date
from decimal import Decimal
import pytest
from employees.models import Employee
from employees.services import get_reporting_rate, normalize_to_usd

@pytest.fixture
def employee(db):
    rate = get_reporting_rate("USD")
    return Employee.objects.create(
        employee_id="EMP00001", first_name="Ava", last_name="Stone", email="ava@acme.example",
        department="Engineering", job_title="Backend Engineer", job_level="SENIOR", country="United States",
        currency="USD", annual_salary=Decimal("120000"), exchange_rate_to_usd=rate,
        annual_salary_usd=normalize_to_usd(Decimal("120000"), rate), hire_date=date(2022, 1, 1),
    )

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
