from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Max, Min

from employees.models import Employee
from departments.models import Department


class DashboardAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        employees = Employee.objects.filter(is_deleted=False)

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
        }

        return Response(data)
