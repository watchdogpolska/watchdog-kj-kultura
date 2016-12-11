from django.core.urlresolvers import reverse
from django.test import TestCase

from ..factories import CategoryFactory, OrganizationFactory
from teryt_tree.factories import JednostkaAdministracyjnaFactory


class OrganizationListViewTestCase(TestCase):

    def setUp(self):
        self.default_org = OrganizationFactory(category=None)

    def test_can_view_home(self):
        resp = self.client.get(reverse('organizations:list'))
        self.assertEqual(resp.status_code, 200)

    def test_filter_category(self):
        category = CategoryFactory()
        org_in_cat = OrganizationFactory(category=category)
        org_without_cat = OrganizationFactory(category=None)
        resp = self.client.get(reverse('organizations:list', kwargs={'category': category.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, org_in_cat)
        self.assertNotContains(resp, org_without_cat)

        self.assertContains(resp, category.name)

    def test_filter_teryt(self):
        jst = JednostkaAdministracyjnaFactory()
        org_inside = OrganizationFactory(jst=jst)
        org_outside = OrganizationFactory(jst=JednostkaAdministracyjnaFactory())
        resp = self.client.get(reverse('organizations:list', kwargs={'region': jst.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, org_inside)
        self.assertNotContains(resp, org_outside)

        self.assertContains(resp, jst.name)


class OrganizationDetailViewTestCase(TestCase):

    def setUp(self):
        self.object = OrganizationFactory()
        self.url = self.object.get_absolute_url()

    def test_can_view_self(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
