from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import distribution, grouped, summary

def _serialize(value):
    if hasattr(value, "quantize"): return f"{value:.2f}"
    return value

@api_view(["GET"])
def summary_view(request):
    return Response({k: _serialize(v or 0) for k, v in summary().items()})

@api_view(["GET"])
def by_department(request):
    return Response([{k: _serialize(v or 0) for k, v in row.items()} for row in grouped("department")])

@api_view(["GET"])
def by_country(request):
    return Response([{k: _serialize(v or 0) for k, v in row.items()} for row in grouped("country")])

@api_view(["GET"])
def salary_distribution(request):
    return Response(distribution())
