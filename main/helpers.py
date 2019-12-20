from django.contrib.admin.helpers import ActionForm
from .widgets import BootstrapSelectWidget
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class HRMSActionForm(ActionForm):
    action = forms.ChoiceField(label=_('Action:'), widget=BootstrapSelectWidget)
