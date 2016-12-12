from django.test import TestCase
from django.core import mail
from ..factories import OrganizationFactory, MetaCategoryFactory
from ..forms import OrganizationFixForm
from ...teryt.factories import JednostkaAdministracyjnaFactory
from ...users.factories import UserFactory


class OrganizationFixFormTestCase(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()

    def test_valid_submission(self):
        form = OrganizationFixForm(data={'name': 'exapmle-name',
                                         'email': 'xxx@example.com',
                                         'jst': JednostkaAdministracyjnaFactory().pk,
                                         'category': '',
                                         'sources': 'some-text'},
                                   instance=self.organization)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_add_metacategory(self):
        metacategory = MetaCategoryFactory()
        form = OrganizationFixForm(instance=self.organization)
        self.assertIn('meta_%s' % (metacategory.pk), form.fields)

    def test_send_emails_with_metacategory(self):
        metacategory = MetaCategoryFactory()
        UserFactory(notify_about_fix=True)
        fieldname = 'meta_%s' % (metacategory.pk)
        form = OrganizationFixForm(data={'name': 'exapmle-name',
                                         'email': 'xxx@example.com',
                                         'jst': JednostkaAdministracyjnaFactory().pk,
                                         'category': '',
                                         fieldname: 'REALLY_UNIQUE',
                                         'sources': 'REALLY_SECOND_UNIQUE'},
                                   instance=self.organization)
        self.assertTrue(form.is_valid(), msg=form.errors)
        form.save()
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox.pop()
        for text in ('REALLY_UNIQUE', 'REALLY_SECOND_UNIQUE'):
            self.assertIn('REALLY_UNIQUE', msg.alternatives[0][0])
            self.assertIn('REALLY_UNIQUE', msg.body)
