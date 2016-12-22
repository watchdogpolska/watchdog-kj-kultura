from django.conf import settings


GEOCODE_BAIDU_API_KEY = getattr(settings, 'GEOCODE_BAIDU_API_KEY', None)
GEOCODE_BING_API_KEY = getattr(settings, 'GEOCODE_BING_API_KEY', None)
GEOCODE_GOOGLE_API_KEY = getattr(settings, 'GEOCODE_GOOGLE_API_KEY', None)
GEOCODE_YANDEX_API_KEY = getattr(settings, 'GEOCODE_YANDEX_API_KEY', None)
