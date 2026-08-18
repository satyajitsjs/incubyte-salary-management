# Generated for the take-home project.
import uuid
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("employee_id", models.CharField(db_index=True, max_length=20, unique=True)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("department", models.CharField(db_index=True, max_length=100)),
                ("job_title", models.CharField(max_length=150)),
                ("job_level", models.CharField(choices=[("JUNIOR","Junior"),("MID","Mid"),("SENIOR","Senior"),("STAFF","Staff"),("LEAD","Lead"),("MANAGER","Manager"),("DIRECTOR","Director")], db_index=True, max_length=20)),
                ("country", models.CharField(db_index=True, max_length=100)),
                ("currency", models.CharField(max_length=3)),
                ("annual_salary", models.DecimalField(decimal_places=2, max_digits=14)),
                ("exchange_rate_to_usd", models.DecimalField(decimal_places=6, max_digits=12)),
                ("annual_salary_usd", models.DecimalField(db_index=True, decimal_places=2, max_digits=14)),
                ("hire_date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["employee_id"]},
        ),
        migrations.CreateModel(
            name="SalaryChange",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("previous_salary", models.DecimalField(decimal_places=2, max_digits=14)),
                ("new_salary", models.DecimalField(decimal_places=2, max_digits=14)),
                ("previous_currency", models.CharField(max_length=3)),
                ("new_currency", models.CharField(max_length=3)),
                ("exchange_rate_to_usd", models.DecimalField(decimal_places=6, max_digits=12)),
                ("previous_salary_usd", models.DecimalField(decimal_places=2, max_digits=14)),
                ("new_salary_usd", models.DecimalField(decimal_places=2, max_digits=14)),
                ("effective_date", models.DateField()),
                ("reason", models.CharField(blank=True, max_length=250)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("employee", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="salary_changes", to="employees.employee")),
            ],
            options={"ordering": ["-effective_date", "-created_at"]},
        ),
        migrations.AddIndex(model_name="employee", index=models.Index(fields=["department", "country"], name="employees_e_departm_a930f4_idx")),
        migrations.AddIndex(model_name="employee", index=models.Index(fields=["country", "annual_salary_usd"], name="employees_e_country_4c5f91_idx")),
        migrations.AddIndex(model_name="employee", index=models.Index(fields=["department", "annual_salary_usd"], name="employees_e_departm_c366f1_idx")),
    ]
