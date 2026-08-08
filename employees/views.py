from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm
from .models import Employee


@login_required
def employee_list(request):

    employees = Employee.objects.all()

    search = request.GET.get("search", "").strip()
    department = request.GET.get("department")
    status = request.GET.get("status")
    sort = request.GET.get("sort")

    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search)
            | Q(full_name__icontains=search)
            | Q(email__icontains=search)
            | Q(department__icontains=search)
            | Q(designation__icontains=search)
        )

    if department:
        employees = employees.filter(department=department)

    if status:

        if status == "active":
            employees = employees.filter(is_active=True)

        elif status == "inactive":
            employees = employees.filter(is_active=False)

    if sort:

        if sort == "newest":
            employees = employees.order_by("-created_at")

        elif sort == "oldest":
            employees = employees.order_by("created_at")

        elif sort == "name_asc":
            employees = employees.order_by("full_name")

        elif sort == "name_desc":
            employees = employees.order_by("-full_name")

        elif sort == "salary_desc":
            employees = employees.order_by("-salary")

        elif sort == "salary_asc":
            employees = employees.order_by("salary")

    paginator = Paginator(employees, 10)
    page_number = request.GET.get("page")
    employees = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)
    query_string = query_params.urlencode()

    return render(
        request,
        "employees/list.html",
        {
            "employees": employees,
            "query_string": query_string,
        },
    )


@login_required
@permission_required("employees.add_employee", raise_exception=True)
def employee_create(request):

    if request.method == "POST":

        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():

            employee = form.save(commit=False)

            last_employee = Employee.objects.last()

            if last_employee:

                last_number = int(last_employee.employee_id[3:])
                employee.employee_id = f"EMP{last_number + 1:04d}"

            else:

                employee.employee_id = "EMP0001"

            employee.save()

            messages.success(
                request,
                "Employee added successfully.",
            )

            return redirect("employees:employee_list")

    else:

        form = EmployeeForm()

    return render(
        request,
        "employees/create.html",
        {
            "form": form,
        },
    )


@login_required
def employee_detail(request, id):

    employee = get_object_or_404(Employee, id=id)

    return render(
        request,
        "employees/detail.html",
        {
            "employee": employee,
        },
    )


@login_required
def employee_update(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Employee updated successfully.",
            )

            return redirect(
                "employees:employee_detail",
                id=employee.id,
            )

    else:

        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employees/create.html",
        {
            "form": form,
        },
    )


@login_required
@permission_required("employees.delete_employee", raise_exception=True)
def employee_delete(request, id):

    employee = get_object_or_404(Employee, id=id)

    if request.method == "POST":

        employee.delete()

        messages.success(
            request,
            "Employee deleted successfully.",
        )

        return redirect("employees:employee_list")

    return render(
        request,
        "employees/delete.html",
        {
            "employee": employee,
        },
    )