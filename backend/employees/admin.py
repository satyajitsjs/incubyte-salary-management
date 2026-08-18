from django.contrib import admin
from .models import Employee, SalaryChange

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "first_name", "last_name", "department", "country", "currency", "annual_salary", "annual_salary_usd")
    list_filter = ("department", "country", "job_level", "currency")
    search_fields = ("employee_id", "first_name", "last_name", "email")

@admin.register(SalaryChange)
class SalaryChangeAdmin(admin.ModelAdmin):
    list_display = ("employee", "previous_salary", "previous_currency", "new_salary", "new_currency", "effective_date", "created_at")
    readonly_fields = [field.name for field in SalaryChange._meta.fields]
