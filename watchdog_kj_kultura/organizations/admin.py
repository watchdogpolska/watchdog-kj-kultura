from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .forms import OrganizationAdminForm
from .models import Category, MetaCategory, Organization


@admin.register(MetaCategory)
class MetaCategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for MetaCategory
    '''
    list_display = ('name', 'key')
    search_fields = ('name', 'key')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    '''
        Admin View for Organization
    '''
    list_display = ('name', 'email', 'jst', 'user', 'created', 'modified')
    list_filter = ('created', 'modified')
    readonly_fields = ('meta',)
    search_fields = ('name',)
    form = OrganizationAdminForm

    def get_field_kwargs_for_category(self, category, obj):
        if obj:
            return {'label': category.name,
                    'initial': obj.meta.get(category.key, ''),
                    'help_text': _("Use {{object.meta.{key}}} in templates to display value").
                    format(key=category.key)}
        return dict(label=category.name)

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
