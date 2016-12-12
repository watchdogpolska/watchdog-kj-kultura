from django.views.generic import CreateView, DetailView, ListView
from django.utils.translation import ugettext_lazy as _
from braces.views import SelectRelatedMixin, UserFormKwargsMixin, FormValidMessageMixin
from ..main.views import BreadcrumbsMixin
from ..organizations.models import Organization
from .models import Request, Template
from .forms import RequestForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property


class TemplateListView(ListView):
    model = Template


class OrganizationRequestView(BreadcrumbsMixin, BreadcrumbsMixin,
                              SelectRelatedMixin, FormValidMessageMixin, CreateView):

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

    def get_breadcrumbs(self):
        b = [(_('Organization list'), reverse('organizations:list')), ]
        if self.organization.jst:
            for node in self.organization.jst.get_ancestors(include_self=True):
                b += [(node, reverse('organizations:list', kwargs={'region': str(node.slug)})), ]
        b += [(self.organization.object, self.organization.get_absolute_url())]
        b += [(self.template, None)]
        return b


class RequestDetailView(BreadcrumbsMixin, SelectRelatedMixin, DetailView):
    model = Request
    select_related = ['organization', ]


class RequestCreateView(BreadcrumbsMixin, FormValidMessageMixin, UserFormKwargsMixin, CreateView):
    model = Request
    form_class = RequestForm

    def get_form_valid_message(self):
        return _("{0} created!").format(self.object)
