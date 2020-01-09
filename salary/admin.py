from django.contrib import admin
from main.admin import admin_site, HrmsModelAdmin
from salary.forms import SalaryBreakupForm
from .models import SalaryComponent, SalaryPackage, SalaryBreakup

# Register your models here.


@admin.register(SalaryComponent, site=admin_site)
class SalaryComponentAdmin(HrmsModelAdmin):
    pass


class SalaryBreakupInline(admin.TabularInline):
    model = SalaryBreakup
    extra = 0
    form = SalaryBreakupForm


@admin.register(SalaryPackage, site=admin_site)
class SalaryPackageAdmin(HrmsModelAdmin):
    fieldsets = (
        ('', {'fields': (
            ('employee', 'appraisal_date', 'is_current'),
        )}),
    )
    list_display = ('employee', 'appraisal_date', 'ctc', 'is_current')
    search_fields = ('employee', 'appraisal_date', 'ctc')
    inlines = [SalaryBreakupInline]
