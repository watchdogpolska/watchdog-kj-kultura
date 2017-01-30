from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class HasJSTListFilter(admin.SimpleListFilter):
    title = _('Has JST')
    parameter_name = 'jst'

    def lookups(self, request, model_admin):
        return (
            ('null', _('Is null')),
            ('value', _('Has value')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'null':
            return queryset.filter(jst__isnull=True)
        if self.value() == 'value':
            return queryset.filter(jst__isnull=False)
