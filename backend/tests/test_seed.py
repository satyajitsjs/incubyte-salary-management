import pytest
from django.core.management import call_command
from employees.models import Employee

@pytest.mark.django_db
def test_seed_creates_requested_count():
    call_command("seed_employees", count=25, seed=7)
    assert Employee.objects.count() == 25
    assert Employee.objects.filter(employee_id="EMP00001").exists()

@pytest.mark.django_db
def test_seed_is_reproducible():
    call_command("seed_employees", count=2, seed=7)
    first=list(Employee.objects.order_by("employee_id").values_list("country","annual_salary"))
    call_command("seed_employees", count=2, seed=7, reset=True)
    second=list(Employee.objects.order_by("employee_id").values_list("country","annual_salary"))
    assert first == second
