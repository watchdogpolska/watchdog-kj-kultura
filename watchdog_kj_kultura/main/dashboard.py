"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'watchdog-kj-kultura.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard import Dashboard, modules
# from grappelli.dashboard.utils import get_admin_site_name
from ..organizations_requests.dashboardmodules import RecentRequest


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        # site_name = get_admin_site_name(context)
        EDITORIAL = ('watchdog_kj_kultura.*.*',
                     'teryt_tree.*')
        # append an app list module for "Editorial Section"
        self.children.append(modules.AppList(
            _("Editorial Section"),
            collapsible=False,
            column=1,
            models=EDITORIAL,
        ))

        # append a group for "Administration Section"
        self.children.append(modules.AppList(
            _('Administration Section'),
            collapsible=True,
            css_classes=('grp-collapse', 'grp-closed',),
            column=1,
            exclude=EDITORIAL,
        ))

        # append a recent actions module
        self.children.append(RecentRequest(
            limit=10,
            collapsible=False,
            column=3,
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            column=2,
            children=[
                {
                    'title': _('Citizens Network Watchdog Poland'),
                    'url': 'http://siecobywatelska.pl/',
                    'external': True,
                },
                {
                    'title': _('watchdog-kj-kultura Documentation'),
                    'url': 'https://watchdog-kj-kultura.readthedocs.io/pl/latest/',
                    'external': True,
                },
                {
                    'title': _('watchdog-kj-kultura code'),
                    'url': 'https://github.com/watchdogpolska/watchdog-kj-kultura',
                    'external': True,
                },
            ]
        ))
