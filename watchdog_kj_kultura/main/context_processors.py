from django.contrib.sites.shortcuts import get_current_site
from .models import Settings


def settings(request):
    """A context processor which provide current site ``Settings`` in ``settings`` template variable

    Parameters
    ----------
    request : HttpRequest
        A django standard request object
    """
    return {'settings': Settings.objects.get(site=get_current_site(request))}
