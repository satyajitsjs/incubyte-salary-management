from datetime import date
from decimal import Decimal
import pytest
from employees.models import Employee
from employees.services import get_reporting_rate, normalize_to_usd

def make_emp(i, department, country, salary):
    rate = get_reporting_rate("USD")
    return Employee.objects.create(employee_id=f"T{i:03d}", first_name=f"Name{i}", last_name="Tester", email=f"t{i}@acme.example", department=department, job_title="Engineer", job_level="MID", country=country, currency="USD", annual_salary=Decimal(str(salary)), exchange_rate_to_usd=rate, annual_salary_usd=normalize_to_usd(Decimal(str(salary)),rate), hire_date=date(2023,1,1))

@pytest.mark.django_db
def test_employee_list_is_paginated(api_client):
    for i in range(30): make_emp(i, "Engineering", "India", 50000+i)
    data = api_client.get("/api/employees/").json()
    assert data["count"] == 30 and len(data["results"]) == 25

@pytest.mark.django_db
def test_combined_filters(api_client):
    make_emp(1,"Engineering","India",70000); make_emp(2,"Engineering","Canada",90000); make_emp(3,"Product","India",80000)
    data = api_client.get("/api/employees/?department=Engineering&country=India").json()
    assert data["count"] == 1 and data["results"][0]["employee_id"] == "T001"

@pytest.mark.django_db
def test_search_matches_job_title(api_client):
    emp = make_emp(4,"Engineering","India",80000); emp.job_title="Platform Specialist"; emp.save()
    data=api_client.get("/api/employees/?search=platform").json()
    assert data["count"] == 1

@pytest.mark.django_db
def test_salary_range_filter(api_client):
    make_emp(1,"Engineering","India",40000); make_emp(2,"Engineering","India",80000); make_emp(3,"Engineering","India",120000)
    data=api_client.get("/api/employees/?salary_min=70000&salary_max=100000").json()
    assert [x["employee_id"] for x in data["results"]] == ["T002"]

@pytest.mark.django_db
def test_invalid_ordering_falls_back_safely(api_client):
    make_emp(2,"Engineering","India",50000); make_emp(1,"Engineering","India",50000)
    data=api_client.get("/api/employees/?ordering=__unsafe").json()
    assert [x["employee_id"] for x in data["results"]] == ["T001","T002"]

@pytest.mark.django_db
def test_salary_history_endpoint(api_client, employee):
    response=api_client.patch(f"/api/employees/{employee.id}/", {"annual_salary":"125000"}, format="json")
    assert response.status_code == 200
    history=api_client.get(f"/api/employees/{employee.id}/salary_history/").json()
    assert len(history) == 1
