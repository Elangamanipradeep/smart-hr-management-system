from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Employee
from .pagination import EmployeePagination
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status

from accounts.permissions import (
    IsAdmin,
    IsAdminOrHR,
)


class EmployeeListCreateAPIView(ListCreateAPIView):

    permission_classes = [IsAuthenticated, IsAdminOrHR]

    queryset = Employee.objects.filter(is_deleted=False)

    serializer_class = EmployeeSerializer

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    pagination_class = EmployeePagination

    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]

    search_fields = [
        "full_name",
        "department__name",
        "designation",
    ]

    filterset_fields = [
        "department",
        "designation",
        "is_active",
    ]

    ordering_fields = [
        "salary",
        "joining_date",
        "full_name",
    ]


class EmployeeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated, IsAdminOrHR]

    queryset = Employee.objects.filter(is_deleted=False)

    serializer_class = EmployeeSerializer

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def destroy(self, request, *args, **kwargs):

        if not request.user.groups.filter(name="Admin").exists():

            return Response(
                {
                    "error": "Only Admin can delete employees."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        employee = self.get_object()

        employee.is_deleted = True

        employee.save()

        return Response(
            {
                "message": "Employee deleted successfully."
            },
            status=status.HTTP_200_OK,
        )
