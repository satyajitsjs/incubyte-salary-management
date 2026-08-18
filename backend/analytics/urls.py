from django.urls import path
from . import views
urlpatterns = [
    path("summary/", views.summary_view),
    path("by_department/", views.by_department),
    path("by_country/", views.by_country),
    path("salary_distribution/", views.salary_distribution),
]
