from django.contrib.auth.forms import UserCreationForm
from .models import Employee


class EmployeeCreationForm(UserCreationForm):

    class Meta:
        model = Employee
        fields = ("username",)

    def save(self, commit=True):
        return Employee.objects.create_user(
            self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password1")
        )

    def save_m2m(self):
        pass
