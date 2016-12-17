from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Element
from grappelli.forms import GrappelliSortableHiddenMixin


class ElementInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    '''
        Tabular Inline View for Element
    '''
    model = Element


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    '''
        Admin View for Element
    '''
    list_display = ('name', 'url', 'is_external_url', 'get_children_count')
    list_filter = ('created', 'modified')
    search_fields = ('name', 'url')
    exclude = ('parent', )
    inlines = [ElementInline]

    def get_queryset(self, *args, **kwargs):
        qs = super(ElementAdmin, self).get_queryset(*args, **kwargs)
        return qs.filter(parent=None).with_children_count()

    def get_children_count(self, obj):
        return obj.children_count
    get_children_count.short_description = _('Children count')
