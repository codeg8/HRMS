from django import forms
from django.conf import settings


class BootstrapSelectWidget(forms.Select):

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-select/css/bootstrap-select%s.css' % extra]}
        js = [
            'assets/global/plugins/bootstrap-select/js/bootstrap-select%s.js' % extra,
            'assets/pages/scripts/components-bootstrap-select%s.js' % extra
        ]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None, choices=()):
        final_attrs = {'class': 'bs-select'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, choices=choices)


class HRMSRadioSelect(forms.RadioSelect):
    template_name = 'admin/widgets/abc.html'

    def __init__(self, attrs=None, choices=()):
        final_attrs = {'class': 'md-radiobtn'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=attrs, choices=choices)


class DatePicker(forms.TextInput):

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-datepicker/css/bootstrap-datepicker3%s.css' % extra]}
        js = [
            'assets/global/plugins/bootstrap-datepicker/js/bootstrap-datepicker%s.js' % extra,
            'assets/pages/scripts/components-date-time-pickers%s.js' % extra
        ]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'date-picker'}
        if attrs is not None and 'class' in attrs:
            final_attrs['class'] += ' ' + attrs['class']
            #final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class TimePicker(forms.TextInput):

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-timepicker/js/bootstrap-timepicker%s.css' % extra]}
        js = ['assets/global/plugins/bootstrap-timepicker/js/bootstrap-timepicker%s.js' % extra]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'time-picker'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class DateTimePicker(forms.TextInput):

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-datetimepicker/js/bootstrap-datetimepicker%s.css' % extra]}
        js = ['assets/global/plugins/bootstrap-datetimepicker/js/bootstrap-datetimepicker%s.js' % extra]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'date-time-picker'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class DateRangePicker(forms.TextInput):

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-daterangepicker/daterangepicker%s.css' % extra]}
        js = ['assets/global/plugins/bootstrap-daterangepicker/daterangepicker%s.js' % extra]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None):
        final_attrs = {'class': 'date-range-picker'}
        if attrs is not None:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs)


class BootstrapSwitchInput(forms.CheckboxInput):

    # template_name = 'main/widgets/switch.html'

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        css = {'all': ['assets/global/plugins/bootstrap-switch/css/bootstrap-switch%s.css' % extra]}
        js = [
            'assets/global/plugins/bootstrap-switch/js/bootstrap-switch%s.js' % extra,
        ]
        return forms.Media(js=js, css=css)

    def __init__(self, attrs=None, check_test=None):
        final_attrs = {'class': 'make-switch'}

        if attrs is not None:
            attrs['class'] = final_attrs['class'] + attrs.get('class')
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, check_test=check_test)


class AdminRadioSelect(forms.RadioSelect):
    template_name = 'admin/main/widgets/radio.html'
