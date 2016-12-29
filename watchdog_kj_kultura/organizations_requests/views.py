from django.views.generic import CreateView, DetailView, ListView
from django.utils.translation import ugettext_lazy as _
from braces.views import SelectRelatedMixin, FormValidMessageMixin
from ..main.views import BreadcrumbsMixin
from ..organizations.models import Organization
from .models import Request, Template
from .forms import RequestForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property


class OrganizationMixin(object):

    @cached_property
    def organization(self):
        return get_object_or_404(Organization.objects.select_related('jst'),
                                 slug=self.kwargs['organization'])

    def get_context_data(self, **kwargs):
        context = super(OrganizationMixin, self).get_context_data(**kwargs)
        context['organization'] = self.organization
        return context


class RequestCreateView(BreadcrumbsMixin, SelectRelatedMixin, FormValidMessageMixin,
                        CreateView):

    model = Request
    select_related = ['category', 'jst']
    form_class = RequestForm

    @cached_property
    def template(self):
        return get_object_or_404(Template, slug=self.kwargs['template'])

    @cached_property
    def organization(self):
        return get_object_or_404(Organization.objects.select_related('jst'),
                                 slug=self.kwargs['organization'])

    def get_form_kwargs(self):
        kwargs = super(RequestCreateView, self).get_form_kwargs()
        kwargs.update({'organization': self.organization,
                       'template': self.template,
                       'request': self.request})
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(RequestCreateView, self).get_context_data(*args, **kwargs)
        context.update({'organization': self.organization,
                        'template': self.template})
        return context

    def get_form_valid_message(self):
        return _("Requests to {organization} was sent!").format(organization=self.organization)

    def get_breadcrumbs(self):
        b = [(_('Organization list'), reverse('organizations:list')), ]
        if self.organization.jst:
            for node in self.organization.jst.get_ancestors(include_self=True):
                b += [(node, reverse('organizations:list', kwargs={'region': str(node.slug)})), ]
        b += [(self.organization, self.organization.get_absolute_url())]
        b += [(self.template, None)]
        return b


class RequestDetailView(BreadcrumbsMixin, SelectRelatedMixin, DetailView):
    model = Request
    select_related = ['organization', 'organization__jst']

    def get_breadcrumbs(self):
        b = [(_('Organization list'), reverse('organizations:list')), ]
        if self.object.organization.jst:
            for node in self.object.organization.jst.get_ancestors(include_self=True):
                b += [(node, reverse('organizations:list', kwargs={'region': str(node.slug)})), ]
        b += [(self.object.organization, self.object.organization.get_absolute_url())]
        b += [(self.object, None)]
        return b
