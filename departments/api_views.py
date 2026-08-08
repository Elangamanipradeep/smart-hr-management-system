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


class DepartmentListCreateAPIView(ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    
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
    
    
class DepartmentRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):

    permission_classes = [IsAuthenticated]

    queryset = Department.objects.all()

    serializer_class = DepartmentSerializer
    
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH
        """
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)