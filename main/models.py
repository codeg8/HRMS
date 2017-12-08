from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from .model_manager import EmployeeManager


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)


class Designation(Group):

    class Meta:
        proxy = True
        verbose_name = 'designation'
        verbose_name_plural = 'designations'


class Employee(AbstractUser):
    department = models.OneToOneField(Department, on_delete=models.SET_NULL, null=True)
    position = models.OneToOneField(Designation, on_delete=models.SET_NULL, null=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='manger', null=True)

    REQUIRED_FIELDS = []
    objects = EmployeeManager()

