from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MainConfig(AppConfig):
    name = 'watchdog_kj_kultura.main'
    verbose_name = _("Main module")
