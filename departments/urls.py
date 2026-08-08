from django.urls import path
from . import api_views

app_name = "departments"

urlpatterns = [
    path(
        "api/departments/",
        api_views.DepartmentListCreateAPIView.as_view(),
        name="department-list-create",
    ),

    path(
        "api/departments/<int:pk>/",
        api_views.DepartmentRetrieveUpdateDestroyAPIView.as_view(),
        name="department-detail",
    ),
]