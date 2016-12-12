from django.core.urlresolvers import reverse
from django.test import TestCase

from ..factories import TemplateFactory, NotificationFactory, RequestFactory, EventFactory
from ...organizations.factories import OrganizationFactory


class TemplateListViewTestCase(TestCase):

    def setUp(self):
        self.template = TemplateFactory()
        self.organization = OrganizationFactory()
        self.url = reverse('organizations_requests:templates',
                           kwargs={'organization': self.organization.slug})

    def test_status_code_for_home(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_contains_link_to_organization(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.organization.get_absolute_url())

    def test_contains_organization_name(self):
        resp = self.client.get(self.url)
        self.assertContains(resp, self.organization)

    def test_contains_link_to_template(self):
        resp = self.client.get(self.url)
        url = reverse('organizations_requests:send',
                      kwargs={'organization': self.organization.slug,
                              'template': self.template.slug})
        self.assertContains(resp, url)


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

    def test_contains_link_to_template_list(self):
        resp = self.client.get(self.url)
        url = reverse('organizations_requests:templates',
                      kwargs={'organization': self.organization.slug})
        self.assertContains(resp, url)


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

    def test_contains_link_to_template_list(self):
        resp = self.client.get(self.url)
        url = reverse('organizations_requests:templates',
                      kwargs={'organization': self.request.organization.slug})
        self.assertContains(resp, url)
