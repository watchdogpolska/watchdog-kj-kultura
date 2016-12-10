from braces.views import SelectRelatedMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from .models import Category, Organization
from teryt_tree.models import JednostkaAdministracyjna


class BreadcrumbsMixin:

    def get_breadcrumbs(self):
        return [(_('Organization list'), None), ]

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class OrganizationListView(BreadcrumbsMixin, SelectRelatedMixin, ListView):
    model = Organization
    select_related = ['category']

    @property
    def is_category(self):
        return 'category' in self.kwargs

    @property
    def is_teryt(self):
        return 'teryt' in self.kwargs

    def get_template_name_suffix(self):
        if self.is_category:
            return '_category'
        if self.is_teryt:
            return '_teryt'
        return '_list'

    def get_breadcrumbs(self):
        if self.is_category:
            return [(_('Organization list'), reverse('organizations:list')),
                    (self.category, None),
                    ]
        if self.is_teryt:
            return [(_('Organization list'), reverse('organizations:list')),
                    (self.teryt, None),
                    ]
        return [(_('Organization list'), None),
                ]

    @cached_property
    def category(self):
        return (get_object_or_404(Category, slug=self.kwargs['category'])
                if 'category' in self.kwargs else None)

    @cached_property
    def teryt(self):
        return (get_object_or_404(JednostkaAdministracyjna, slug=self.kwargs['teryt'])
                if 'teryt' in self.kwargs else None)

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['teryt'] = self.teryt
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(category=self.category) if 'category' in self.kwargs else qs
        qs = qs.filter(jst=self.teryt) if 'teryt' in self.kwargs else qs
        return qs


class OrganizationDetailView(BreadcrumbsMixin, SelectRelatedMixin, DetailView):
    model = Organization
    select_related = ['category', ]

    def get_breadcrumbs(self):
        b = [(_('Organization list'), reverse('organizations:list')), ]
        if self.object.category:
            b += [(self.object.category, self.object.category.get_absolute_url), ]
        b += [(self.object, None), ]
        print(b)
        return b
