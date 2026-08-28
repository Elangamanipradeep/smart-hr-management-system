from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):

    employee_count = serializers.SerializerMethodField()
    
    class Meta:

        model = Department

        fields = [
            "id",
            "department_code",
            "name",
            "description",
            "employee_count",
            "created_at",
            "updated_at",
        ]
        
        read_only_fields = [
            "department_code",
            "employee_count",
            "created_at",
            "updated_at",
        ]

    def get_employee_count(self, obj):

        return obj.employees.filter(is_deleted=False).count()