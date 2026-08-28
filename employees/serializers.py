from rest_framework import serializers
from datetime import date
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    employee_id = serializers.CharField(read_only=True)

    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:

        model = Employee

        fields = "__all__"

    def validate_phone(self, value):
        
        if not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain only digits."
            )
            
        if len(value) != 10:
            raise serializers.ValidationError(
                "Phone number must be exactly 10 digits."
            )

        return value

    
    def validate_salary(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                "Salary must be greater than 0."
            )

        return value
    
    def validate_joining_date(self, value):

        if value > date.today():
            raise serializers.ValidationError(
                "Joining date cannot be in the future."
            )

        return value
    
    def validate(self, attrs):

        department = attrs.get(
            "department",
            getattr(self.instance, "department", None)
        )

        designation = attrs.get(
            "designation",
            getattr(self.instance, "designation", None)
        )

        if (
            department
            and designation
            and department.name == "HR"
            and designation == "Backend Developer"
        ):

            raise serializers.ValidationError(
                "Backend Developers cannot belong to the HR department."
            )

        return attrs