from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrganizationsRequestsConfig(AppConfig):
    name = 'watchdog_kj_kultura.organizations_requests'
    verbose_name = _("Requests to organizations system")
