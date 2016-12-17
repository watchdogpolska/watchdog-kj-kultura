from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MenuConfig(AppConfig):
    name = 'watchdog_kj_kultura.menu'
    verbose_name = _("Menu module")
