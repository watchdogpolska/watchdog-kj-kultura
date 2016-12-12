from django.core.exceptions import ImproperlyConfigured


class BreadcrumbsMixin(object):

    def get_breadcrumbs(self):
        raise ImproperlyConfigured(
            '{0} is missing a breadcrumbs. Define override ' +
            '{0}.get_url().'.format(self.__class__.__name__))

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context
