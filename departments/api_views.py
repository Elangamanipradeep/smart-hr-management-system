from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Department
from .pagination import DepartmentPagination
from .serializers import DepartmentSerializer
from rest_framework.response import Response

from accounts.permissions import (
    IsAdmin,
    IsAdminOrHR,
)
from rest_framework import status


class DepartmentListCreateAPIView(ListCreateAPIView):
    
    permission_classes = [
        IsAuthenticated,
        IsAdminOrHR,
    ]
    
    queryset = Department.objects.all()
    
    serializer_class = DepartmentSerializer
    
    pagination_class = DepartmentPagination
    
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    
    search_fields = [
        "name",
        "description",
    ]

    filterset_fields = [
        "name",
    ]

    ordering_fields = [
        "name",
        "created_at",
    ]
    
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get("all") == "true":

            serializer = self.get_serializer(queryset, many=True)

            return Response(serializer.data)

        return super().list(request, *args, **kwargs)
    
    
class DepartmentRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [
            IsAuthenticated,
            IsAdminOrHR,
        ]

    queryset = Department.objects.all()

    serializer_class = DepartmentSerializer
    
    def partial_update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return self.update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):

        department = self.get_object()

        employee_count = department.employees.filter(
            is_deleted=False
        ).count()

        if employee_count > 0:

            return Response(
                {
                    "error": (
                        f"Cannot delete department because it has "
                        f"{employee_count} employee(s). "
                        f"Please move the employees to another department first."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        department.delete()

        return Response(
            {
                "message": "Department deleted successfully."
            },
            status=status.HTTP_200_OK,
        )