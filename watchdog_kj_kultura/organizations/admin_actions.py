from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from geopy.geocoders import Nominatim, Baidu, Bing, GoogleV3, Yandex
from .settings import (GEOCODE_BAIDU_API_KEY, GEOCODE_BING_API_KEY,
                       GEOCODE_GOOGLE_API_KEY, GEOCODE_YANDEX_API_KEY)


GEOCODERS_LIST = ['Nominatim', 'Baidu', 'Bing', 'Google', 'Yandex']


def get_geocoder_for_service(service):
    """For the service provided, try to return a geocoder instance.

    Args:
        service (string): name of service
    Returns:
        geopy.geocoders.geocoders.base.Geocoder: instance of geocoder initialized with
            appropriate API key
    """
    service = service.strip().lower()
    if service == 'nominatim':
        useragent = ','.join("%s <%s>" % x for x in settings.ADMINS)
        return Nominatim(user_agent=useragent)
    if service == 'baidu' and GEOCODE_BAIDU_API_KEY:
        return Baidu(GEOCODE_BAIDU_API_KEY)
    if service == 'bing' and GEOCODE_BING_API_KEY:
        return Bing(GEOCODE_BING_API_KEY)
    if service == 'google' and GEOCODE_GOOGLE_API_KEY:
        return GoogleV3(GEOCODE_GOOGLE_API_KEY)
    if service == 'yandex' and GEOCODE_YANDEX_API_KEY:
        return Yandex(GEOCODE_YANDEX_API_KEY, 'en_US')


class GeocodeOrganizationAction(object):

    @classmethod
    def list_supported(self):
        """Returns all configured services

        Returns:
            dict: service-instances of GeocodeOrganizationAction
        """
        geocoder = {}
        for name in GEOCODERS_LIST:
            service = get_geocoder_for_service(name)
            if service:
                description = _("Geocode using %s") % (name)
                geocoder[name] = GeocodeOrganizationAction.as_action(short_description=description,
                                                                     geocoder=service)
        return geocoder

    def __init__(self, admin, geocoder=None):
        self.geocoder = geocoder or self.get_geocoder_for_service('nominatim')
        self.admin = admin

    def update(self):
        geocoded = skipped = 0
        for organization in self.queryset:
            point = self.geocoder.geocode(organization.geocode_input(), language='pl')
            if point:
                organization.set_geopy_point(point)
                organization.save(update_fields=["pos"])
                geocoded += 1
            else:
                skipped += 1
        return (skipped, geocoded)

    def result(self, skipped, geocoded):
        msg = _("In action {geocoded} organizations was " +
                "geocoded, {skipped} skipped").format(geocoded, skipped)
        messages.success(self.request, msg)

    def execute(self, request, queryset):
        self.request = request
        self.queryset = queryset
        return self.result(*self.update())

    @classmethod
    def as_action(cls, short_description, geocoder, *args, **kwargs):
        def action(admin, request, queryset):
            self = cls(admin=admin, geocoder=geocoder, *args, **kwargs)
            return self.execute(request, queryset)
        action.short_description = short_description
        return action
