from braces.views import SelectRelatedMixin
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView

from .models import Category, Organization
from teryt_tree.models import JednostkaAdministracyjna


class MenuMixin(object):

    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class BreadcrumbsMixin(object):

    def get_breadcrumbs(self):
        return [(_('Organization list'), None), ]

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class OrganizationListView(MenuMixin, BreadcrumbsMixin, SelectRelatedMixin, ListView):
    model = Organization
    select_related = ['category']

    @property
    def is_category(self):
        return 'category' in self.kwargs

    @property
    def is_region(self):
        return 'region' in self.kwargs

    def get_template_name_suffix(self):
        if self.is_category:
            return '_category'
        if self.is_region:
            return '_region'
        return '_list'

    def get_breadcrumbs(self):
        if self.is_category:
            return [(_('Organization list'), reverse('organizations:list')),
                    (self.category, None), ]
        if self.is_region:
            return [(_('Organization list'), reverse('organizations:list')),
                    (self.region, None), ]
        return [(_('Organization list'), None), ]

    @cached_property
    def category(self):
        return (get_object_or_404(Category, slug=self.kwargs['category'])
                if self.is_category else None)

    @cached_property
    def region(self):
        return (get_object_or_404(JednostkaAdministracyjna, slug=self.kwargs['region'])
                if self.is_region else None)

    def get_context_data(self, **kwargs):
        context = super(OrganizationListView, self).get_context_data(**kwargs)
        context['category'] = self.category
        context['region'] = self.region
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationListView, self).get_queryset(*args, **kwargs)
        qs = qs.filter(category=self.category) if self.is_category else qs
        qs = qs.area(self.region) if self.is_region else qs
        return qs


class OrganizationDetailView(MenuMixin, BreadcrumbsMixin, SelectRelatedMixin, DetailView):
    model = Organization
    select_related = ['category', ]

    def get_breadcrumbs(self):
        b = [(_('Organization list'), reverse('organizations:list')), ]
        if self.object.category:
            b += [(self.object.category, self.object.category.get_absolute_url), ]
        b += [(self.object, None), ]
        print(b)
        return b
