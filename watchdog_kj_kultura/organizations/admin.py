from django import forms
from django.conf import settings
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
    list_display = ('name', 'email', 'jst', 'user', 'created', 'modified', 'pos', )
    list_filter = ('created', 'modified')
    readonly_fields = ('meta',)
    search_fields = ('name',)
    actions = ('geocode_location', 'geocode_clean', 'switch_visible')
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

    def get_geocoder_useragent(self):
        return ','.join("%s <%s>" % x for x in settings.ADMINS)

    def geocode_location(self, request, queryset):
        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent=self.get_geocoder_useragent())
        geocoded = 0
        skipped = 0
        for organization in queryset:
            point = geolocator.geocode(organization.geocode_input(), language='pl')
            if point:
                organization.set_geopy_point(point)
                organization.save(update_fields=["pos"])
                geocoded += 1
            else:
                skipped += 1
        print("%s geocoded, %d skipped" % (geocoded, skipped))
    geocode_location.short_description = _("Geocode selected using Nominatim")

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
