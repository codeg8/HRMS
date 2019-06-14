from django.apps import apps
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import AdminSite
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.db import router, transaction, models
from django.forms.forms import BoundField
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse, NoReverseMatch
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from main import widgets as my_widgets
from django.forms import widgets
from .helpers import HRMSActionForm
from .forms import EmployeeCreationForm, EmployeeChangeForm, AdminLoginForm
from .models import Designation, Employee, Department

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


HORIZONTAL, VERTICAL = 1, 2


def get_ul_class(radio_style):
    return 'radiolist' if radio_style == VERTICAL else 'radiolist inline'


# Function to add a control-label class to the labels
def add_control_label(f):
    def control_label_tag(self, contents=None, attrs=None, label_suffix=None):
        print('MONKEYYYYYYYYY')
        if attrs is None:
            attrs = {}
        attrs['class'] = 'control-label'
        return f(self, contents, attrs, label_suffix)

    return control_label_tag


# MonkeyPath the label_tag to add the control Label
BoundField.label_tag = add_control_label(BoundField.label_tag)

# Override the default AdminSite Class to customize
class HRMSAdminSite(AdminSite):
    login_form = AdminLoginForm
    index_title = _('Dashboard')

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'icon': model._meta.icon,
                'perms': perms,
            }
            if perms.get('change'):
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def index(self, request, extra_context=None):
        """
                Display the main admin index page, which lists all of the installed
                apps that have been registered in this site.
                """
        context = dict(
            self.each_context(request),
            title=self.index_title,
            sub_heading='dashboard & statics'
        )
        context.update(extra_context or {})
        request.current_app = self.name
        return TemplateResponse(request, self.index_template or 'admin/index.html', context)

    def each_context(self, request):
        result = super(HRMSAdminSite, self).each_context(request)
        result.update({'app_list': self.get_app_list(request)})
        return result




admin_site = HRMSAdminSite(name='HRMS-admin')


class HrmsModelAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {'widget': widgets.TextInput(attrs={'class': 'form-control'})},
        models.IntegerField: {'widget': widgets.NumberInput(attrs={'class': 'form-control'})},
        models.FloatField: {'widget': widgets.NumberInput(attrs={'class': 'form-control'})},
        models.EmailField: {'widget': widgets.EmailInput(attrs={'class': 'form-control'})},
        models.TextField: {'widget': widgets.Textarea(attrs={'class': 'form-control'})},
        models.BooleanField: {'widget': widgets.CheckboxInput(attrs={'class': 'make-switch form-control'})},
        # TODO: Create widgets for below Fields
        # models.DateField: {'widget': widgets.Textarea(attrs={'class': 'form-control'})},
        # models.DateTimeField: {'widget': widgets.Textarea(attrs={'class': 'form-control'})},
        # models.FilePathField: {},
        # models.TimeField: {}
    }

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Get a form Field for a database Field that has declared choices.
        """
        # If the field is named as a radio_field, use a RadioSelect
        if db_field.name in self.radio_fields:
            # Avoid stomping on custom widget/choices arguments.
            if 'widget' not in kwargs:
                kwargs['widget'] = my_widgets.AdminRadioSelect(attrs={
                    'class': get_ul_class(self.radio_fields[db_field.name]),
                })
            if 'choices' not in kwargs:
                kwargs['choices'] = db_field.get_choices(
                    include_blank=db_field.blank,
                    blank_choice=[('', _('None'))]
                )
        return db_field.formfield(**kwargs)

    action_form = HRMSActionForm

    def changelist_view(self, request, extra_context=None):
        cl = self.get_changelist_instance(request)
        extra_context = dict(
            title=capfirst(cl.opts.verbose_name_plural),
            icon=cl.opts.icon
        )
        return super(HrmsModelAdmin, self).changelist_view(request, extra_context)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Get a form Field for a database Field that has declared choices.
        """
        # If the field is named as a radio_field, use a RadioSelect
        if db_field.name in self.radio_fields:
            # Avoid stomping on custom widget/choices arguments.
            # if 'widget' not in kwargs:
            #     kwargs['widget'] = my_widgets.AdminRadioSelect(attrs={
            #         'class': get_ul_class(self.radio_fields[db_field.name]),
            #     })
            if 'choices' not in kwargs:
                kwargs['choices'] = db_field.get_choices(
                    include_blank=db_field.blank,
                    blank_choice=[('', _('None'))]
                )
                kwargs['widget'] = my_widgets.BootstrapSelectWidget(attrs={
                    'class': get_ul_class(self.radio_fields[db_field.name]),
                }, choices=kwargs['choices'])
        return db_field.formfield(**kwargs)


@admin.register(Designation, site=admin_site)
class DesignationAdmin(HrmsModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)


@admin.register(Employee, site=admin_site)
class EmployeeAdmin(HrmsModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    date_hierarchy = 'date_joined'
    readonly_fields = ('username', 'password', 'email')
    fieldsets = (
        (_('Account info'), {'fields': (('username', 'email'),)}),
        (_('Personal info'), {
            'fields': (
                ('first_name', 'last_name'),
                ('gender', 'dob'),
                'address',
            )
        }),
        (_('Employment info'), {
            'fields': (('date_joined', 'department'), ('groups', 'manager'))
        }),
        (_('Permissions'), {
            'fields': (
                ('is_active', 'is_superuser'),
                'user_permissions'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    form = EmployeeChangeForm
    add_form = EmployeeCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('emp_id', 'full_name', 'username', 'email', 'department', 'groups',
                    'manager', 'is_active', 'is_superuser')
    list_filter = ('department', 'groups', 'is_superuser', 'is_active', )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # list_editable = ('email', )
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)
    radio_fields = {"gender": admin.HORIZONTAL}

    def has_change_permission(self, request, obj=None):
        # Allow if user is trying to update his own details.
        if request.user == obj:
            return True
        else:
            return super(EmployeeAdmin, self).has_change_permission(request, obj)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    def lookup_allowed(self, lookup, value):
        # See #20078: we don't want to allow any lookups involving passwords.
        if lookup.startswith('password'):
            return False
        return super().lookup_allowed(lookup, value)

    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)

    def _add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, It is mandatory that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set. Please contact admin.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': username_field.help_text,
        }
        extra_context.update(defaults)
        return super().add_view(request, form_url, extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext('Password changed successfully.')
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _('Change password: %s') % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST = request.POST.copy()
            request.POST['_continue'] = 1
        return super().response_add(request, obj, post_url_continue)


@admin.register(Department, site=admin_site)
class DepartmentAdmin(HrmsModelAdmin):
    list_per_page = 4
