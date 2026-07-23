from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        
        model = Employee
        
        fields = [
            "full_name",
            "email",
            "phone",
            "department",
            "designation",
            "salary",
            "joining_date",
            "is_active",
            "profile_photo",
        ]
        
        widgets = {
           
             "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Full Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number"
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Department"
                }
            ),

            "designation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Designation"
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Salary"
                }
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
            
        }
                
    def clean_salary(self):

        salary = self.cleaned_data["salary"]

        if salary < 0:

            raise forms.ValidationError(
                "Salary cannot be negative."
            )

        return salary
    
    def clean_full_name(self):
        
        full_name = self.cleaned_data["full_name"].strip()
        
        
        if len(full_name) < 3:
            
            raise forms.ValidationError(
                "Full name must contain at least 3 characters."
            )
        
        words = full_name.split()
        
        for word in words:
            
            if not word.isalpha():
                
                raise forms.ValidationError(
                    "Full name can contain only letters and spaces."
                )
            
            
        return full_name.title()
    
    def clean_phone(self):
        
        phone = self.cleaned_data["phone"].strip()
        
        if len(phone) != 10:
            
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )
        
        if not phone.isdigit():
            
            raise forms.ValidationError(
                "Phone must be Numbers"
            )
        
        return phone
    
    
    def clean_profile_photo(self):

        photo = self.cleaned_data["profile_photo"]

        if photo:

            if photo.size > 2 * 1024 * 1024:

                raise forms.ValidationError(
                    "Image size must be less than 2 MB."
                )

            if not photo.name.lower().endswith(
                (".jpg", ".jpeg", ".png")
            ):

                raise forms.ValidationError(
                    "Only JPG, JPEG and PNG images are allowed."
                )

        return photo
        
    
    def clean(self):

        cleaned_data = super().clean()

        department = cleaned_data.get("department")
        salary = cleaned_data.get("salary")

        if department and salary:

            if department.lower() == "intern" and salary > 30000:

                raise forms.ValidationError(
                    "Intern salary cannot be greater than ₹30,000."
                )

        return cleaned_data