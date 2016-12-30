from django.contrib.sitemaps import Sitemap
from .models import Organization


class OrganizationSitemap(Sitemap):

    def items(self):
        return Organization.objects.visible().all()

    def lastmod(self, obj):
        return obj.modified
