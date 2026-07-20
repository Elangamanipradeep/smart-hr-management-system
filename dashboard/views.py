from django.shortcuts import render
from employees.models import Employee
from django.db.models import Count, Sum, Avg, Max, Min
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):

    total_employees = Employee.objects.count()

    active_employees = Employee.objects.filter(is_active=True).count()

    inactive_employees = Employee.objects.filter(is_active=False).count()

    total_departments = Employee.objects.values("department").distinct().count()

    total_salary = Employee.objects.aggregate(total_salary=Sum("salary"))

    average_salary = Employee.objects.aggregate(average_salary=Avg("salary"))

    highest_salary = Employee.objects.aggregate(highest_salary=Max("salary"))

    lowest_salary = Employee.objects.aggregate(lowest_salary=Min("salary"))

    department_statistics = Employee.objects.values("department").annotate(
        total=Count("department")
    )

    labels = []
    data = []

    for department_data in department_statistics:
        labels.append(department_data["department"])
        data.append(department_data["total"])

    context = {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,
        "total_departments": total_departments,
        "department_statistics": department_statistics,
        "labels": labels,
        "data": data,
        "total_salary": total_salary,
        "average_salary": average_salary,
        "highest_salary": highest_salary,
        "lowest_salary": lowest_salary,
    }

    return render(request, "dashboard/index.html", context)
