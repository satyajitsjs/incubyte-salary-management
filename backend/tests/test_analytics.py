from datetime import date
from decimal import Decimal
import pytest
from employees.models import Employee
from employees.services import get_reporting_rate, normalize_to_usd

def add(i, dept, country, usd):
    r=get_reporting_rate("USD")
    return Employee.objects.create(employee_id=f"A{i}", first_name="A", last_name=str(i), email=f"a{i}@acme.example", department=dept, job_title="Role", job_level="MID", country=country, currency="USD", annual_salary=Decimal(str(usd)), exchange_rate_to_usd=r, annual_salary_usd=normalize_to_usd(Decimal(str(usd)),r), hire_date=date(2024,1,1))

@pytest.mark.django_db
def test_summary_average_median_and_total(api_client):
    add(1,"Engineering","India",50000); add(2,"Engineering","India",100000); add(3,"Product","Canada",150000)
    data=api_client.get("/api/analytics/summary/").json()
    assert data["employee_count"] == 3
    assert Decimal(data["total_payroll_usd"]) == Decimal("300000.00")
    assert Decimal(data["average_salary_usd"]) == Decimal("100000.00")
    assert Decimal(data["median_salary_usd"]) == Decimal("100000.00")

@pytest.mark.django_db
def test_department_grouping(api_client):
    add(1,"Engineering","India",100000); add(2,"Engineering","Canada",50000); add(3,"Product","India",80000)
    rows=api_client.get("/api/analytics/by_department/").json()
    eng=next(x for x in rows if x["department"]=="Engineering")
    assert eng["employee_count"] == 2 and Decimal(eng["total_payroll_usd"]) == Decimal("150000.00")

@pytest.mark.django_db
def test_country_grouping(api_client):
    add(1,"Engineering","India",100000); add(2,"Product","India",50000); add(3,"Product","Canada",80000)
    rows=api_client.get("/api/analytics/by_country/").json()
    india=next(x for x in rows if x["country"]=="India")
    assert india["employee_count"] == 2

@pytest.mark.django_db
def test_distribution_counts_every_employee_once(api_client):
    for i,s in enumerate([20000,40000,60000,90000,120000,175000,250000]): add(i,"Engineering","India",s)
    rows=api_client.get("/api/analytics/salary_distribution/").json()
    assert sum(x["employee_count"] for x in rows) == 7
