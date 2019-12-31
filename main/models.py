from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .model_manager import EmployeeManager
from django.utils.translation import ugettext_lazy as _
from config.settings import COMPANY_EMP_ID_FORMAT
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('icon',)


# Create your models here.
class Department(models.Model):

    class Meta:
        icon = _('icon-grid')

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Designation(Group):

    class Meta:
        proxy = True
        db_table = _('main_designation')
        verbose_name = _('designation')
        verbose_name_plural = _('designations')
        icon = _('icon-badge')


class Employee(AbstractUser):
    class Meta:
        verbose_name = _('employee')
        verbose_name_plural = _('employees')
        icon = _('icon-users')

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=False)
    address = models.TextField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    groups = models.ForeignKey(
        Designation,
        verbose_name=_('Designation'),
        on_delete=models.SET_NULL,
        null=True,
        help_text=_('Default Permission for different modules in Portal depends upon employee\'s Designation.')
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
        _('superuser'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name=_('manger'),
        null=True,
        blank=True,
    )
    REQUIRED_FIELDS = []
    objects = EmployeeManager()

    def __str__(self):
        return self.emp_id() + " <" + self.username + ">"

    def emp_id(self):
        return COMPANY_EMP_ID_FORMAT[0] + str(self.pk).zfill(COMPANY_EMP_ID_FORMAT[1])
    emp_id.admin_order_field = 'pk'

    def full_name(self):
        return self.first_name + " " + self.last_name
