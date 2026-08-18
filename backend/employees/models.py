import uuid
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db import models
from .services import SUPPORTED_CURRENCIES, get_reporting_rate, normalize_to_usd


class Employee(models.Model):
    LEVELS = [
        ("JUNIOR", "Junior"),
        ("MID", "Mid"),
        ("SENIOR", "Senior"),
        ("STAFF", "Staff"),
        ("LEAD", "Lead"),
        ("MANAGER", "Manager"),
        ("DIRECTOR", "Director"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.CharField(max_length=20, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, db_index=True)
    job_title = models.CharField(max_length=150)
    job_level = models.CharField(max_length=20, choices=LEVELS, db_index=True)
    country = models.CharField(max_length=100, db_index=True)
    currency = models.CharField(max_length=3)
    annual_salary = models.DecimalField(max_digits=14, decimal_places=2)
    exchange_rate_to_usd = models.DecimalField(max_digits=12, decimal_places=6)
    annual_salary_usd = models.DecimalField(max_digits=14, decimal_places=2, db_index=True)
    hire_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["employee_id"]
        indexes = [
            models.Index(fields=["department", "country"]),
            models.Index(fields=["country", "annual_salary_usd"]),
            models.Index(fields=["department", "annual_salary_usd"]),
        ]

    def clean(self):
        if self.annual_salary is None or self.annual_salary <= Decimal("0"):
            raise ValidationError({"annual_salary": "Annual salary must be greater than zero."})
        if self.currency not in SUPPORTED_CURRENCIES:
            raise ValidationError({"currency": f"Unsupported currency: {self.currency}."})

    def save(self, *args, **kwargs):
        self.currency = self.currency.upper()
        if not self.exchange_rate_to_usd:
            self.exchange_rate_to_usd = get_reporting_rate(self.currency)
        self.annual_salary_usd = normalize_to_usd(self.annual_salary, self.exchange_rate_to_usd)
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return f"{self.employee_id} — {self.full_name}"


class SalaryChange(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, related_name="salary_changes", on_delete=models.CASCADE)
    previous_salary = models.DecimalField(max_digits=14, decimal_places=2)
    new_salary = models.DecimalField(max_digits=14, decimal_places=2)
    previous_currency = models.CharField(max_length=3)
    new_currency = models.CharField(max_length=3)
    exchange_rate_to_usd = models.DecimalField(max_digits=12, decimal_places=6)
    previous_salary_usd = models.DecimalField(max_digits=14, decimal_places=2)
    new_salary_usd = models.DecimalField(max_digits=14, decimal_places=2)
    effective_date = models.DateField()
    reason = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-effective_date", "-created_at"]

    def __str__(self):
        return f"{self.employee.employee_id}: {self.previous_salary} {self.previous_currency} → {self.new_salary} {self.new_currency}"
