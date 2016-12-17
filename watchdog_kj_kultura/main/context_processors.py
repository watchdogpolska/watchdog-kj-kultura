from django.contrib.sites.shortcuts import get_current_site
from .models import Settings


def settings(request):
    return {'settings': Settings.objects.get(site=get_current_site(request))}
