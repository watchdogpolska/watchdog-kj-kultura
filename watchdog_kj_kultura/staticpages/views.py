from braces.views import SelectRelatedMixin
from django.views.generic import DetailView

from ..main.views import BreadcrumbsMixin
from .models import Page


class PageDetailView(BreadcrumbsMixin, SelectRelatedMixin, DetailView):
    model = Page
    select_related = ['user', ]

    def get_breadcrumbs(self):
        b = []
        if self.object.parent:
            for node in self.object.parent.get_ancestors(include_self=True).filter(visible=True):
                b += [(node, node.get_absolute_url()), ]
        b += [(self.object, None)]
        return b

    def get_queryset(self, *args, **kwargs):
        qs = super(PageDetailView, self).get_queryset(*args, **kwargs)
        return qs.filter(visible=True)
