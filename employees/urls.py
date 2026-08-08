from django.urls import path

from . import api_views
from . import views

app_name = "employees"

urlpatterns = [

    # -----------------------
    # Django Template Views
    # -----------------------

    path(
        "employees/",
        views.employee_list,
        name="employee_list",
    ),

    path(
        "create/",
        views.employee_create,
        name="employee_create",
    ),

    path(
        "<int:id>/",
        views.employee_detail,
        name="employee_detail",
    ),

    path(
        "<int:id>/edit/",
        views.employee_update,
        name="employee_update",
    ),

    path(
        "<int:id>/delete/",
        views.employee_delete,
        name="employee_delete",
    ),

    # -----------------------
    # REST API
    # -----------------------

    path(
        "api/employees/",
        api_views.EmployeeListCreateAPIView.as_view(),
        name="employee-list-create",
    ),

    path(
        "api/employees/<int:pk>/",
        api_views.EmployeeRetrieveUpdateDestroyAPIView.as_view(),
        name="employee-detail",
    ),
]