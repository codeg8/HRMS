from django.db import models
from main.models import Employee
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class SalaryComponent(models.Model):
    class Meta:
        icon = _('fa fa-reorder')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SalaryPackage(models.Model):
    class Meta:
        icon = _('fa fa-money')
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name=_('salary'),
        null=False,
    )
    ctc = models.FloatField(verbose_name="Total CTC", null=False)
    appraisal_date = models.DateField(verbose_name="Appraisal Date", null=False)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return str(self.employee) + ' Salary Package for FY ' + str(self.appraisal_date.year) + ' - ' + str(self.appraisal_date.year + 1)


class SalaryBreakup(models.Model):
    class Meta:
        icon = _('fa fa-credit-card')
    COMPONENT_PAY_FREQUENCY_CHOICES = (
        ('D', _('Daily')),
        ('W', _('Weekly')),
        ('M', _('Monthly')),
        ('Q', _('Quarterly')),
        ('S', _('Semi Annually')),
        ('A', _('Annually')),
    )
    package = models.ForeignKey(
        SalaryPackage,
        on_delete=models.CASCADE,
        related_name=_('CTC_Breakup'),
        null=False,
    )
    component = models.ForeignKey(
        SalaryComponent,
        on_delete=models.DO_NOTHING,
        related_name=_('Package_Component'),
        null=False
    )
    pay_frequency = models.CharField(max_length=30, choices=COMPONENT_PAY_FREQUENCY_CHOICES, default='M')
    amount = models.FloatField()
