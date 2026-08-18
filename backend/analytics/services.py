from decimal import Decimal
from statistics import median
from django.db.models import Avg, Count, Sum, Min, Max
from employees.models import Employee


def summary():
    agg = Employee.objects.aggregate(
        employee_count=Count("id"), total_payroll_usd=Sum("annual_salary_usd"),
        average_salary_usd=Avg("annual_salary_usd"), min_salary_usd=Min("annual_salary_usd"), max_salary_usd=Max("annual_salary_usd"),
    )
    salaries = list(Employee.objects.order_by("annual_salary_usd").values_list("annual_salary_usd", flat=True))
    agg["median_salary_usd"] = Decimal(str(median(salaries))) if salaries else Decimal("0")
    return agg


def grouped(field):
    return list(Employee.objects.values(field).annotate(
        employee_count=Count("id"), total_payroll_usd=Sum("annual_salary_usd"), average_salary_usd=Avg("annual_salary_usd")
    ).order_by("-total_payroll_usd", field))


def distribution():
    buckets = [(0, 30000), (30000, 50000), (50000, 75000), (75000, 100000), (100000, 150000), (150000, 200000), (200000, None)]
    result = []
    for low, high in buckets:
        qs = Employee.objects.filter(annual_salary_usd__gte=low)
        if high is not None: qs = qs.filter(annual_salary_usd__lt=high)
        result.append({"label": f"${low//1000}k–${high//1000}k" if high else f"${low//1000}k+", "min": low, "max": high, "employee_count": qs.count()})
    return result
