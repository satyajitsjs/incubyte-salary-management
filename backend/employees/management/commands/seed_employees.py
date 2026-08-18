import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker
from employees.models import Employee, SalaryChange
from employees.services import get_reporting_rate, normalize_to_usd

COUNTRIES = {
    "India": ("INR", Decimal("1500000")),
    "United States": ("USD", Decimal("95000")),
    "United Kingdom": ("GBP", Decimal("65000")),
    "Germany": ("EUR", Decimal("70000")),
    "Singapore": ("SGD", Decimal("90000")),
    "Canada": ("CAD", Decimal("85000")),
    "Australia": ("AUD", Decimal("100000")),
    "Japan": ("JPY", Decimal("8500000")),
}
DEPARTMENTS = {
    "Engineering": ["Software Engineer", "Backend Engineer", "Frontend Engineer", "Data Engineer", "QA Engineer"],
    "Product": ["Product Manager", "Product Analyst", "Product Designer"],
    "Sales": ["Account Executive", "Sales Development Representative", "Sales Manager"],
    "Marketing": ["Marketing Specialist", "Growth Manager", "Content Strategist"],
    "Finance": ["Financial Analyst", "Accountant", "Finance Manager"],
    "People": ["HR Generalist", "Recruiter", "People Partner"],
    "Operations": ["Operations Analyst", "Program Manager", "Operations Manager"],
    "Customer Success": ["Customer Success Manager", "Support Specialist", "Implementation Consultant"],
}
LEVEL_MULTIPLIER = {
    "JUNIOR": Decimal("0.60"), "MID": Decimal("0.85"), "SENIOR": Decimal("1.15"),
    "STAFF": Decimal("1.45"), "LEAD": Decimal("1.55"), "MANAGER": Decimal("1.60"), "DIRECTOR": Decimal("2.10"),
}
LEVEL_WEIGHTS = [30, 28, 22, 7, 5, 6, 2]

class Command(BaseCommand):
    help = "Seed deterministic synthetic employee compensation data."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=10000)
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument("--reset", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        if count <= 0 or count > 100000:
            raise CommandError("count must be between 1 and 100000")
        if options["reset"]:
            SalaryChange.objects.all().delete(); Employee.objects.all().delete()
        if Employee.objects.exists():
            raise CommandError("Employees already exist. Use --reset to replace synthetic data.")

        rng = random.Random(options["seed"])
        fake = Faker(); Faker.seed(options["seed"])
        levels = list(LEVEL_MULTIPLIER)
        countries = list(COUNTRIES)
        departments = list(DEPARTMENTS)
        employees = []
        today = date(2026, 8, 18)

        for i in range(1, count + 1):
            country = rng.choices(countries, weights=[38, 18, 9, 9, 8, 7, 6, 5], k=1)[0]
            currency, base = COUNTRIES[country]
            department = rng.choices(departments, weights=[38, 10, 12, 8, 7, 7, 9, 9], k=1)[0]
            level = rng.choices(levels, weights=LEVEL_WEIGHTS, k=1)[0]
            title = rng.choice(DEPARTMENTS[department])
            if level in {"LEAD", "MANAGER", "DIRECTOR"} and "Manager" not in title:
                title = f"{level.title()} {title}"
            variance = Decimal(str(rng.uniform(0.85, 1.15)))
            salary = (base * LEVEL_MULTIPLIER[level] * variance).quantize(Decimal("100"), rounding=ROUND_HALF_UP)
            rate = get_reporting_rate(currency)
            first, last = fake.first_name(), fake.last_name()
            employees.append(Employee(
                employee_id=f"EMP{i:05d}", first_name=first, last_name=last,
                email=f"{first}.{last}.{i}@acme.example".lower().replace("'", "").replace(" ", ""),
                department=department, job_title=title, job_level=level, country=country,
                currency=currency, annual_salary=salary, exchange_rate_to_usd=rate,
                annual_salary_usd=normalize_to_usd(salary, rate),
                hire_date=today - timedelta(days=rng.randint(30, 3650)),
            ))
        Employee.objects.bulk_create(employees, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f"Seeded {count} synthetic employees (seed={options['seed']})."))
