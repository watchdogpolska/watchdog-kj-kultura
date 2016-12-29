from django.core.urlresolvers import reverse
from django.test import TestCase

from ..factories import TemplateFactory, RequestFactory
from ...organizations.factories import OrganizationFactory


class RequestCreateViewTestCase(TestCase):

    def setUp(self):
        self.template = TemplateFactory()
        self.organization = OrganizationFactory()
        self.url = reverse('organizations_requests:send',
                           kwargs={'organization': self.organization.slug,
                                   'template': self.template.slug})

    def test_status_code_for_home(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_contains_link_to_organization(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.organization.get_absolute_url())

    def test_contains_organization_name(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.organization)


class RequestDetailViewTestCase(TestCase):

    def setUp(self):
        self.request = RequestFactory()
        self.url = reverse('organizations_requests:details',
                           kwargs={'pk': str(self.request.pk)})

    def test_status_code_for_home(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_contains_link_to_organization(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.request.organization.get_absolute_url())

    def test_contains_organization_name(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.request.organization)
