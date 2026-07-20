from django.db import models

# Create your models here.


class Employee(models.Model):

    employee_id = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_photo = models.ImageField(
        upload_to="employee_photos/", blank=True, null=True
    )

    def save(self, *args, **kwargs):

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
