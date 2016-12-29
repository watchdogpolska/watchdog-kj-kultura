# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from . import views

urlpatterns = [
    url(_(r'^organization-(?P<organization>[\w\d-]+)/(?P<template>[\w\d-]+)$'),
        views.RequestCreateView.as_view(),
        name="send"),
    url(_(r'^request-(?P<pk>[\d]+)$'), views.RequestDetailView.as_view(),
        name="details"),
]
