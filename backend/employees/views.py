from decimal import Decimal, InvalidOperation
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .importer import import_employee_csv
from .models import Employee
from .serializers import EmployeeSerializer, SalaryChangeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()
    ordering_fields = {"employee_id", "first_name", "last_name", "department", "country", "job_title", "job_level", "annual_salary_usd", "hire_date"}

    def get_queryset(self):
        qs = Employee.objects.all()
        p = self.request.query_params
        search = (p.get("search") or "").strip()
        if search:
            qs = qs.filter(Q(employee_id__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(email__icontains=search) | Q(job_title__icontains=search))
        if p.get("department"):
            qs = qs.filter(department=p["department"])
        if p.get("country"):
            qs = qs.filter(country=p["country"])
        if p.get("job_level"):
            qs = qs.filter(job_level=p["job_level"])
        for param, lookup in (("salary_min", "annual_salary_usd__gte"), ("salary_max", "annual_salary_usd__lte")):
            if p.get(param):
                try:
                    qs = qs.filter(**{lookup: Decimal(p[param])})
                except InvalidOperation:
                    pass
        ordering = p.get("ordering", "employee_id")
        field = ordering.removeprefix("-")
        if field not in self.ordering_fields:
            ordering = "employee_id"
        return qs.order_by(ordering, "employee_id" if field != "employee_id" else "id")

    @action(detail=True, methods=["get"])
    def salary_history(self, request, pk=None):
        employee = self.get_object()
        return Response(SalaryChangeSerializer(employee.salary_changes.all(), many=True).data)

    @action(detail=False, methods=["get"])
    def metadata(self, request):
        return Response({
            "departments": list(Employee.objects.order_by("department").values_list("department", flat=True).distinct()),
            "countries": list(Employee.objects.order_by("country").values_list("country", flat=True).distinct()),
            "job_levels": [{"value": value, "label": label} for value, label in Employee.LEVELS],
        })

    @action(detail=False, methods=["post"], url_path="import_csv")
    def import_csv(self, request):
        uploaded = request.FILES.get("file")
        if not uploaded:
            return Response({"detail": "Attach a CSV file in multipart field 'file'."}, status=status.HTTP_400_BAD_REQUEST)
        if not uploaded.name.lower().endswith(".csv"):
            return Response({"detail": "Only .csv files are supported."}, status=status.HTTP_400_BAD_REQUEST)
        result = import_employee_csv(uploaded)
        if result.errors:
            return Response({"imported": 0, "errors": result.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"imported": result.imported, "errors": []}, status=status.HTTP_201_CREATED)
