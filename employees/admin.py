from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "full_name",
        "department",
        "designation",
        "salary",
        "is_active",
    )

    search_fields = (
        "employee_id",
        "full_name",
        "email",
    )

    list_filter = (
        "department",
        "is_active",
    )

    ordering = ("employee_id",)
