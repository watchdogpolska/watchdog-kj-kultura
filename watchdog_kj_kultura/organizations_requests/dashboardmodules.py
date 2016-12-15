from django.utils.translation import ugettext_lazy as _
from grappelli.dashboard.modules import DashboardModule

from ..organizations_requests.models import Request


class RecentRequest(DashboardModule):
    """
    Module that lists the recent requests

    Attributes
    ----------

    children : ``QuerySet``
        It contains list of :class:`watchdog_kj_kultura.organizations.models.Organization` to shows for user
    limit : int
        Number of objects return
    template : str
        Template name to render of module in dasbhard
    title : str
        Title of module in dashboard
    """

    title = _('Recent Actions')
    template = 'grappelli/dashboard/modules/recent_request.html'
    limit = 25

    def __init__(self, title=None, limit=10, include_list=None,
                 exclude_list=None, **kwargs):
        title = title or _('Recent requests')
        kwargs.update({'limit': limit})
        super(RecentRequest, self).__init__(title, **kwargs)
        qs = Request.objects.order_by('created').select_related('organization').all()
        self.children = qs[:self.limit]
