from datetime import date
from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Employee, SalaryChange
from .services import SUPPORTED_CURRENCIES, get_reporting_rate, normalize_to_usd


class SalaryChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryChange
        fields = ["id", "previous_salary", "new_salary", "previous_currency", "new_currency", "exchange_rate_to_usd", "previous_salary_usd", "new_salary_usd", "effective_date", "reason", "created_at"]


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    annual_salary_usd = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
    exchange_rate_to_usd = serializers.DecimalField(max_digits=12, decimal_places=6, read_only=True)
    salary_effective_date = serializers.DateField(write_only=True, required=False)
    salary_change_reason = serializers.CharField(write_only=True, required=False, allow_blank=True, max_length=250)

    class Meta:
        model = Employee
        fields = [
            "id", "employee_id", "first_name", "last_name", "full_name", "email",
            "department", "job_title", "job_level", "country", "currency",
            "annual_salary", "exchange_rate_to_usd", "annual_salary_usd", "hire_date",
            "created_at", "updated_at", "salary_effective_date", "salary_change_reason",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_currency(self, value):
        value = value.upper()
        if value not in SUPPORTED_CURRENCIES:
            raise serializers.ValidationError(f"Unsupported currency. Choose one of: {', '.join(SUPPORTED_CURRENCIES)}")
        return value

    def validate_annual_salary(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("Annual salary must be greater than zero.")
        return value

    def create(self, validated_data):
        validated_data.pop("salary_effective_date", None)
        validated_data.pop("salary_change_reason", None)
        currency = validated_data["currency"]
        validated_data["exchange_rate_to_usd"] = get_reporting_rate(currency)
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        effective_date = validated_data.pop("salary_effective_date", date.today())
        reason = validated_data.pop("salary_change_reason", "")
        previous_salary = instance.annual_salary
        previous_currency = instance.currency
        previous_rate = instance.exchange_rate_to_usd
        previous_salary_usd = instance.annual_salary_usd

        requested_currency = validated_data.get("currency", instance.currency).upper()
        if requested_currency != instance.currency:
            validated_data["exchange_rate_to_usd"] = get_reporting_rate(requested_currency)
        elif "annual_salary" in validated_data:
            validated_data["exchange_rate_to_usd"] = instance.exchange_rate_to_usd

        employee = super().update(instance, validated_data)
        salary_changed = employee.annual_salary != previous_salary or employee.currency != previous_currency
        if salary_changed:
            SalaryChange.objects.create(
                employee=employee,
                previous_salary=previous_salary,
                new_salary=employee.annual_salary,
                previous_currency=previous_currency,
                new_currency=employee.currency,
                exchange_rate_to_usd=employee.exchange_rate_to_usd,
                previous_salary_usd=previous_salary_usd,
                new_salary_usd=normalize_to_usd(employee.annual_salary, employee.exchange_rate_to_usd),
                effective_date=effective_date,
                reason=reason,
            )
        return employee
