from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from main import widgets
from main.widgets import DatePicker
from .models import Employee
from django import forms
from django.contrib.admin.widgets import AdminDateWidget
import datetime

class AdminLoginForm(AuthenticationForm):
    pass
    # redirect('admin:auth_user_password_change', id=user.pk)


class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ("username",)

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

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

    # BIRTH_YEAR_CHOICES = tuple(_ for _ in range(1950, datetime.datetime.now().year))

    # dob = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES), label='Date of Birth',
    # required=False)
    dob = forms.DateField(widget=DatePicker(attrs={"class": 'form-control'}), label='Date of Birth')
    date_joined = forms.DateField(widget=DatePicker(attrs={"class": 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 30, "class": 'form-control'}),
                              required=False)

    def __init__(self, *args, **kwargs):
        super(EmployeeChangeForm, self).__init__(*args, **kwargs)
        self.empID = self.instance.id
        self.fields['manager'].queryset = Employee.objects.filter(~Q(id=self.empID))

    def clean_manager(self):
        # An Employee Cannot have himself assigned as a manager
        mgr = self.cleaned_data["manager"]
        if self.instance == mgr:
            raise ValidationError("Employee needs to have a different manager")
        return mgr


class CommentForm(forms.Form):
    name = forms.CharField(widget=widgets.BootstrapSelectWidget(choices=(('M', 'Male'), ('F', 'Female'))))
    url = forms.URLField()
    comment = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))
