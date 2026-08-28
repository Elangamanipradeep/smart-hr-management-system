from django.db import models
from django.db.models import Max

class Department(models.Model):

    name = models.CharField(
        max_length=100, 
        unique=True
    )
    
    description = models.TextField(
        blank=True,
        null=True,
    )
    
    department_code = models.CharField(
        max_length=10,
        blank=True,
        unique=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):

        if not self.department_code:

            last_department = Department.objects.aggregate(
                Max("department_code")
            )["department_code__max"]

            if last_department:

                last_number = int(last_department.replace("DEP", ""))

                self.department_code = f"DEP{last_number + 1:04d}"

            else:

                self.department_code = "DEP0001"

        super().save(*args, **kwargs)