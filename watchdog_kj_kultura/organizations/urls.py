# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.OrganizationListView.as_view(),
        name="list"),
    url(r'^data.geojson$', views.OrganizationMapLayer.as_view(), name='data'),
    url(r'^data-(?P<z>\d+)-(?P<x>\d+)-(?P<y>\d+).geojson$',
        views.OrganizationTiledGeoJSONLayerView.as_view(), name='data'),
    url(_(r'^region-(?P<region>[\w-]+)$'), views.OrganizationListView.as_view(),
        name="list"),
    url(_(r'^organization-(?P<slug>[\w-]+)$'), views.OrganizationDetailView.as_view(),
        name="details"),
    url(r'^(?P<category>[\w-]+)$', views.OrganizationListView.as_view(),
        name="list"),
]
