from django.core.urlresolvers import reverse
from django.test import TestCase

from ..factories import CategoryFactory, OrganizationFactory, MetaCategoryFactory
from teryt_tree.factories import JednostkaAdministracyjnaFactory
from watchdog_kj_kultura.organizations_requests.factories import TemplateFactory


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

    def test_contains_link_to_fix(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('organizations:fix', kwargs={'slug': self.object.slug}))

    def test_contains_link_to_template(self):
        template = TemplateFactory()
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('organizations_requests:send',
                                          kwargs={'organization': self.object.slug,
                                                  'template': template.slug}))
        self.assertContains(resp, template.description)
        self.assertContains(resp, template.name)


class OrganizationFixViewTestCase(TestCase):

    def setUp(self):
        self.meta = MetaCategoryFactory()
        self.object = OrganizationFactory(meta={self.meta.key: 'LOREM_IPSUM'})
        self.url = reverse('organizations:fix', kwargs={'slug': self.object.slug})

    def test_can_view_self(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)

    def test_contains_link_to_details(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, reverse('organizations:details',
                                          kwargs={'slug': self.object.slug}))

    def test_contains_meta_fields_and_values(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "meta_%s" % (self.meta.pk, ))
        self.assertContains(resp, 'LOREM_IPSUM')

    def test_unsaved_changes(self):
        resp = self.client.post(self.url, {'name': 'exapmle-name',
                                           'email': 'xxx@example.com',
                                           'jst': JednostkaAdministracyjnaFactory().pk,
                                           'sources': 'some-text'})
        self.assertEqual(resp.status_code, 302)
        self.object.refresh_from_db()
        self.assertNotEqual(self.object.name, 'exapmle-name')
