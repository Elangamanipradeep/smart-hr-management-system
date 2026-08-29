from django.db.models import Avg, Count

from employees.models import Employee
from departments.models import Department


def get_hr_analytics():

    employees = Employee.objects.filter(is_deleted=False)

    total_employees = employees.count()

    active_employees = employees.filter(
        is_active=True
    ).count()

    inactive_employees = employees.filter(
        is_active=False
    ).count()

    average_salary = employees.aggregate(
        average=Avg("salary")
    )["average"]

    highest_paid = employees.order_by(
        "-salary"
    ).first()

    lowest_paid = employees.order_by(
        "salary"
    ).first()

    department_distribution = (
        employees
        .values("department__name")
        .annotate(employee_count=Count("id"))
        .order_by("-employee_count")
    )

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,
        "average_salary": average_salary,
        "highest_paid_employee": (
            {
                "employee_id": highest_paid.employee_id,
                "name": highest_paid.full_name,
                "salary": str(highest_paid.salary),
                "department": highest_paid.department.name,
            }
            if highest_paid
            else None
        ),
        "lowest_paid_employee": (
            {
                "employee_id": lowest_paid.employee_id,
                "name": lowest_paid.full_name,
                "salary": str(lowest_paid.salary),
                "department": lowest_paid.department.name,
            }
            if lowest_paid
            else None
        ),
        "department_distribution": [
            {
                "department": item["department__name"],
                "employee_count": item["employee_count"],
            }
            for item in department_distribution
        ],
    }