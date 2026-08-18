from datetime import date
from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from employees.models import Employee, SalaryChange
from employees.serializers import EmployeeSerializer
from employees.services import get_reporting_rate, normalize_to_usd

@pytest.mark.django_db
def test_salary_is_normalized_on_save():
    emp = Employee.objects.create(employee_id="E2", first_name="Ira", last_name="Das", email="ira@acme.example", department="Product", job_title="PM", job_level="MID", country="India", currency="INR", annual_salary=Decimal("1000000"), exchange_rate_to_usd=get_reporting_rate("INR"), annual_salary_usd=Decimal("0"), hire_date=date(2024,1,1))
    assert emp.annual_salary_usd == Decimal("11500.00")

@pytest.mark.django_db
def test_zero_salary_is_rejected():
    emp = Employee(employee_id="E3", first_name="No", last_name="Pay", email="no@acme.example", department="Finance", job_title="Analyst", job_level="JUNIOR", country="United States", currency="USD", annual_salary=Decimal("0"), exchange_rate_to_usd=Decimal("1"), annual_salary_usd=Decimal("0"), hire_date=date(2024,1,1))
    with pytest.raises(ValidationError): emp.save()

@pytest.mark.django_db
def test_unsupported_currency_is_rejected():
    emp = Employee(employee_id="E4", first_name="X", last_name="Y", email="xy@acme.example", department="Finance", job_title="Analyst", job_level="JUNIOR", country="X", currency="XYZ", annual_salary=Decimal("100"), exchange_rate_to_usd=Decimal("1"), annual_salary_usd=Decimal("100"), hire_date=date(2024,1,1))
    with pytest.raises(ValidationError): emp.save()

@pytest.mark.django_db
def test_serializer_salary_update_creates_history(employee):
    s = EmployeeSerializer(employee, data={"annual_salary":"130000", "salary_effective_date":"2026-08-18", "salary_change_reason":"Market adjustment"}, partial=True)
    assert s.is_valid(), s.errors
    updated = s.save()
    change = SalaryChange.objects.get(employee=updated)
    assert change.previous_salary == Decimal("120000.00")
    assert change.new_salary == Decimal("130000.00")
    assert change.reason == "Market adjustment"

@pytest.mark.django_db
def test_non_salary_update_does_not_create_history(employee):
    s = EmployeeSerializer(employee, data={"job_title":"Staff Backend Engineer"}, partial=True)
    assert s.is_valid(); s.save()
    assert SalaryChange.objects.count() == 0

@pytest.mark.django_db
def test_currency_change_uses_new_reporting_rate(employee):
    s = EmployeeSerializer(employee, data={"currency":"GBP", "annual_salary":"80000"}, partial=True)
    assert s.is_valid(), s.errors
    updated = s.save()
    assert updated.exchange_rate_to_usd == get_reporting_rate("GBP")
    assert updated.annual_salary_usd == normalize_to_usd(Decimal("80000"), get_reporting_rate("GBP"))
