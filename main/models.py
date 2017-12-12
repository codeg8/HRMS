from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .model_manager import EmployeeManager
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)


class Designation(Group):

    class Meta:
        proxy = True
        db_table = _('main_designation')
        verbose_name = _('designation')
        verbose_name_plural = _('designations')


class Employee(AbstractUser):
    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female'))
    )

    groups = ''  # Override Default Many to many Field.
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    address = models.TextField(max_length=200, null=True)
    department = models.OneToOneField(Department, on_delete=models.SET_NULL, null=True)
    designation = models.OneToOneField(
        Designation,
        on_delete=models.SET_NULL,
        null=True,
        help_text=_(
            'Default Permission for different modules in Portal depends upon employee\'s Designation.'
        )
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('extra permissions'),
        blank=True,
        help_text=_('Any extra permission for this user other than ones already defined for user\'s Designation.<br>'),
        related_name="user_set",
        related_query_name="user",
    )
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    dob = models.DateField(verbose_name="Date of Birth", null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, related_name=_('manger'), null=True)
    REQUIRED_FIELDS = []
    objects = EmployeeManager()

    def full_name(self):
        return self.first_name + " " + self.last_name
