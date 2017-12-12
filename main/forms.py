from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from .models import Employee
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import datetime

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


class EmployeeChangeForm(UserChangeForm):

    class Meta:
        model = Employee
        fields = '__all__'
        field_classes = {'username': UsernameField}

    BIRTH_YEAR_CHOICES = tuple(_ for _ in range(1950, datetime.datetime.now().year))

    dob = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    date_joined = forms.DateField(widget=AdminDateWidget())




