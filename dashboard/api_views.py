from employees.serializers import EmployeeSerializer
from departments.serializers import DepartmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Max, Min, Count, Q

from employees.models import Employee
from departments.models import Department

from accounts.permissions import (
    IsAdmin,
    IsAdminOrHR,
)


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminOrHR]

    def get(self, request):

        employees = Employee.objects.filter(is_deleted=False)
        recent_employees = employees.order_by("-created_at")[:5]
        recent_departments = Department.objects.order_by("-created_at")[:5]
        department_statistics = (
            Department.objects
            .annotate(
                employee_total=Count(
                    "employees",
                    filter=Q(employees__is_deleted=False)
                )
            )
            .values(
                "name",
                "employee_total"
            )
        )
        salary_statistics = employees.aggregate(
            total_salary=Sum("salary"),
            average_salary=Avg("salary"),
            highest_salary=Max("salary"),
            lowest_salary=Min("salary"),
        )

        data = {
            "total_employees": employees.count(),
            "active_employees": employees.filter(is_active=True).count(),
            "inactive_employees": employees.filter(is_active=False).count(),
            "total_departments": Department.objects.count(),
            **salary_statistics,
            "recent_employees": EmployeeSerializer(recent_employees, many=True).data,
            "recent_departments": DepartmentSerializer(
                recent_departments, many=True
            ).data,
            "department_statistics": list(department_statistics),
        }

        return Response(data)
