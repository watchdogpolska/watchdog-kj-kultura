from django import template
from django.core.urlresolvers import reverse
from django.urls.exceptions import NoReverseMatch
register = template.Library()


@register.filter
def object_to_url_edit_obj(obj):
    if obj is None:
        return None
    try:
        return reverse('admin:%s_%s_change' % (obj._meta.app_label,
                                               obj._meta.model_name),
                       args=[obj.pk])
    except (NoReverseMatch, AttributeError):
        return None


@register.filter
def object_list_to_url_edit_obj(object_list):
    if object_list is None:
        return None
    try:
        if None in (object_list.model._meta.app_label, object_list.model._meta.model_name):
            return None
        return reverse('admin:%s_%s_changelist' % (object_list.model._meta.app_label,
                                                   object_list.model._meta.model_name))
    except (NoReverseMatch, AttributeError):
        return None
