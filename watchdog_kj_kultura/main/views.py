from django.core.exceptions import ImproperlyConfigured
from haystack.forms import FacetedSearchForm
from haystack.generic_views import FacetedSearchView
from .compat import get_model
from ..teryt.models import JST


class BreadcrumbsMixin(object):

    def get_breadcrumbs(self):
        raise ImproperlyConfigured(
            '{0} is missing a breadcrumbs. Define override ' +
            '{0}.get_url().'.format(self.__class__.__name__))

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class CustomFacetedSearchView(FacetedSearchView):
    form_class = FacetedSearchForm
    facet_fields = ['jst', 'django_ct']

    def prefetch_jst(self, field):
        ids = [key for key, count in field]
        object_dict = {obj.slug: obj for obj in JST.objects.filter(slug__in=ids).all()}
        return [(object_dict.get(key, key), key, count)
                for key, count in field]

    def prefetch_django_ct(self, field):
        result = []

        for key, count in field:
            model = get_model(*key.split('.', 2))
            name = model._meta.verbose_name_plural
            result.append((name, key, count))
        return result

    def get_context_data(self, *args, **kwargs):
        context = super(CustomFacetedSearchView, self).get_context_data(*args, **kwargs)
        if 'fields' in context['facets']:
            context['jst'] = self.prefetch_jst(context['facets']['fields']['jst'])
            context['django_ct'] = self.prefetch_django_ct(context['facets']['fields']['django_ct'])
        return context
