# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views import defaults as default_views
from django.views.generic import TemplateView
from watchdog_kj_kultura.teryt.sitemaps import JSTSitemap
from watchdog_kj_kultura.organizations.sitemaps import OrganizationSitemap
from watchdog_kj_kultura.staticpages.sitemaps import PageSitemap
from django.contrib.sitemaps import views as sitemap_views

from . import views

sitemaps = {
    'teryt': JSTSitemap,
    'organization': OrganizationSitemap,
    'page': PageSitemap,
}

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),

    url(_(r'^search/'), views.CustomFacetedSearchView.as_view(), name="haystack_search"),

    # User management
    url(_(r'^organizations/'), include('watchdog_kj_kultura.organizations.urls',
                                       namespace='organizations')),
    url(_(r'^region/'), include('watchdog_kj_kultura.teryt.urls', namespace="teryt")),
    url(_(r'^requests/'), include('watchdog_kj_kultura.organizations_requests.urls',
                                  namespace="organizations_requests")),
    url(_(r'^pages/'), include('watchdog_kj_kultura.staticpages.urls', namespace="staticpages")),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^sitemap\.xml$', sitemap_views.index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap_views.sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied,
            kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
