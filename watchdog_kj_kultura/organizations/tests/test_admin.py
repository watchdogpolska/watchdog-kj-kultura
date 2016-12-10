from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from ..admin import OrganizationAdmin
from ..factories import MetaCategoryFactory, OrganizationFactory
from ..models import Organization


class MockRequest(object):
    pass


class MockSuperUser(object):

    def has_perm(self, perm):
        return True


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.categories = [MetaCategoryFactory() for _ in range(0, 5)]
        self.org = OrganizationFactory()

    def test_default_fields(self):
        ma = OrganizationAdmin(Organization, self.site)
        extra = ['meta_%d' % category.pk for category in self.categories]
        fields = ['name', 'email', 'jst', 'user', 'category'] + extra
        # Form contains only editable fields
        self.assertCountEqual(ma.get_form(request).base_fields, fields)
        # Admin contains readonly-fields too
        self.assertCountEqual(ma.get_fields(request), fields + ['meta'])
        self.assertCountEqual(ma.get_fields(request, self.org), fields + ['meta'])
