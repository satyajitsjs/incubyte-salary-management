from io import BytesIO
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from employees.models import Employee

HEADER=b"employee_id,first_name,last_name,email,department,job_title,job_level,country,currency,annual_salary,hire_date\n"

@pytest.mark.django_db
def test_csv_import_success(api_client):
    body=HEADER+b"C001,Ada,Lovelace,ada@acme.example,Engineering,Backend Engineer,SENIOR,United Kingdom,GBP,80000,2024-01-02\n"
    f=SimpleUploadedFile("employees.csv",body,content_type="text/csv")
    r=api_client.post("/api/employees/import_csv/", {"file":f}, format="multipart")
    assert r.status_code == 201 and r.json()["imported"] == 1 and Employee.objects.count() == 1

@pytest.mark.django_db
def test_csv_import_rejects_missing_header(api_client):
    f=SimpleUploadedFile("employees.csv",b"employee_id,email\nC1,a@x.com\n",content_type="text/csv")
    r=api_client.post("/api/employees/import_csv/", {"file":f}, format="multipart")
    assert r.status_code == 400 and r.json()["errors"][0]["field"] == "header"

@pytest.mark.django_db
def test_csv_import_is_all_or_nothing_on_row_error(api_client):
    body=HEADER+b"C001,Ada,Lovelace,ada@acme.example,Engineering,Engineer,SENIOR,United Kingdom,GBP,80000,2024-01-02\n"+b"C002,Bad,Salary,bad@acme.example,Engineering,Engineer,MID,India,INR,-5,2024-01-02\n"
    f=SimpleUploadedFile("employees.csv",body,content_type="text/csv")
    r=api_client.post("/api/employees/import_csv/", {"file":f}, format="multipart")
    assert r.status_code == 400 and Employee.objects.count() == 0

@pytest.mark.django_db
def test_csv_import_rejects_duplicate_employee_id_in_file(api_client):
    row=b"C001,Ada,Lovelace,{email},Engineering,Engineer,SENIOR,United Kingdom,GBP,80000,2024-01-02\n"
    body=HEADER+row.replace(b"{email}",b"one@acme.example")+row.replace(b"{email}",b"two@acme.example")
    f=SimpleUploadedFile("employees.csv",body,content_type="text/csv")
    r=api_client.post("/api/employees/import_csv/", {"file":f}, format="multipart")
    assert r.status_code == 400 and any(e["field"]=="employee_id" for e in r.json()["errors"])
