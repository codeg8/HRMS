from django import forms
from salary.models import SalaryBreakup


class SalaryBreakupForm(forms.ModelForm):
    class Meta:
        model = SalaryBreakup
        fields = '__all__'
        widgets = {
            'component': forms.Select(attrs={'class': 'form-control f-dd '}),
            'pay_frequency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }
