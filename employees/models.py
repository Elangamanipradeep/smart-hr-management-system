from django.db import models
from departments.models import Department
# Create your models here.


class Employee(models.Model):

    employee_id = models.CharField(max_length=10, unique=True, blank=True,)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees", )
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_photo = models.ImageField(
        upload_to="employee_photos/", blank=True, null=True
    )
    
    def save(self, *args, **kwargs):

        # Generate Employee ID
        if not self.employee_id:

            last_employee = Employee.objects.order_by("-id").first()

            if last_employee and last_employee.employee_id:

                last_number = int(last_employee.employee_id[3:])

                self.employee_id = f"EMP{last_number + 1:04d}"

            else:

                self.employee_id = "EMP0001"

        # Delete old profile photo when updating
        if self.pk:

            try:
                old_employee = Employee.objects.get(pk=self.pk)

                if (
                    old_employee.profile_photo
                    and old_employee.profile_photo != self.profile_photo
                ):
                    old_employee.profile_photo.delete(save=False)

            except Employee.DoesNotExist:
                pass

        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):

        if self.profile_photo:
            self.profile_photo.delete(save=False)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"
