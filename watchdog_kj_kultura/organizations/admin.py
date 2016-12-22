from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportMixin

from .admin_actions import GeocodeOrganizationAction
from .forms import OrganizationAdminForm
from .models import Category, MetaCategory, Organization
from .resources import OrganizationResource


class GeocoderActionsMixin(object):
    """Mixins with actions to geocode organizations.
    """

    def get_geocode_actions_list(self):
        """Returns dict of geocoders to appends
        """
        return GeocodeOrganizationAction.list_supported()

    def _get_geocode_action(self, name, func):
        # (function, name, short_description)
        return (func, name, func.short_description)

    def get_actions(self, request):
        actions = super(GeocoderActionsMixin, self).get_actions(request)
        for name, func in self.get_geocode_actions_list().items():
            actions[name] = self._get_geocode_action(name, func)
        return actions


@admin.register(MetaCategory)
class MetaCategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    '''
        Admin View for MetaCategory
    '''
    list_display = ('name', 'key')
    search_fields = ('name', 'key')


@admin.register(Organization)
class OrganizationAdmin(GeocoderActionsMixin, ImportExportMixin, admin.ModelAdmin):
    '''
        Admin View for Organization
    '''
    list_display = ('name', 'email', 'jst', 'user', 'created', 'modified', 'pos', )
    list_filter = ('created', 'modified')
    readonly_fields = ('meta',)
    search_fields = ('name',)
    actions = ('geocode_clean', 'switch_visible',)
    form = OrganizationAdminForm
    resource_class = OrganizationResource
    related_lookup_fields = {
        'fk': ['jst'],
    }

    def get_field_kwargs_for_category(self, category, obj):
        kwargs = dict(label=category.name, required=False)
        if obj:
            HELP = _("Use {{object.meta.{key}}} in templates to display value").\
                format(key=category.key)
            kwargs.update(dict(initial=obj.meta.get(category.key, ''),
                               help_text=HELP))
        return kwargs

    def get_field_for_category(self, *args, **kwargs):
        return forms.CharField(**self.get_field_kwargs_for_category(*args, **kwargs))

    def get_fields(self, request, obj=None):
        gf = super(OrganizationAdmin, self).get_fields(request, obj)
        self.categories = MetaCategory.objects.all()
        self.form.categories = self.categories
        fields = {'meta_%d' % (category.pk): self.get_field_for_category(category, obj)
                  for category in self.categories}
        self.form.declared_fields.update(fields)
        return gf

    def geocode_clean(self, request, queryset):
        queryset.update(pos=None)
    geocode_clean.short_description = _("Clean position of selected")

    def switch_visible(self, request, queryset):
        queryset.switch_visibility()
    switch_visible.short_description = _("Switch visibility of selected")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for Category
    '''
    list_display = ('name', 'get_organization_count')
    search_fields = ('name',)

    def get_organization_count(self, obj):
        return obj.organization_count
    get_organization_count.short_description = _('Organization count')

    def get_queryset(self, *args, **kwargs):
        qs = super(CategoryAdmin, self).get_queryset(*args, **kwargs)
        return qs.with_organization_count()
