from django.core import mail
from django.test import RequestFactory, TestCase

from ...organizations.factories import OrganizationFactory
from ..factories import TemplateFactory
from ..forms import RequestForm


class RequestFormTestCase(TestCase):

    def setUp(self):
        self.organization = OrganizationFactory()
        self.template = TemplateFactory()
        self.factory = RequestFactory()
        self.request = self.factory.get('/customer/details')

    def test_form_is_valid(self):
        body = "Lorem_FOO_BAR_Ipsum"
        form = RequestForm(data={'email': 'jacob@example.com',
                                 'body': body,
                                 'email_user': 'xxxx@example.com'},
                           organization=self.organization,
                           template=self.template,
                           request=self.request)
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_send_email_to_organization(self):
        body = "Lorem_CONTENT_Ipsum"
        form = RequestForm(data={'email': 'jacob@example.com',
                                 'body': body,
                                 'email_user': 'xxxx@example.com'},
                           organization=self.organization,
                           template=self.template,
                           request=self.request)
        self.assertTrue(form.is_valid(), msg=form.errors)
        form.save()
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.organization.email, mail.outbox[0].to)
        self.assertEqual(mail.outbox[0].subject, self.template.subject)
        self.assertIn(body, mail.outbox[0].body)

    def test_send_notification_to_user(self):
        body = "Lorem_CONTENT_Ipsum"
        form = RequestForm(data={'email': 'jacob@example.com',
                                 'body': body,
                                 'email_user': 'xxxx@example.com'},
                           organization=self.organization,
                           template=self.template,
                           request=self.request)
        self.assertTrue(form.is_valid(), msg=form.errors)
        form.save()
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('xxxx@example.com', mail.outbox[1].to)
        self.assertEqual(mail.outbox[1].subject, self.template.subject)
        self.assertIn(body, mail.outbox[1].body)

    def test_require_email_in_body(self):
        kwargs = dict(data={'email': 'jacob@example.com',
                            'body': 'jacob',
                            'email_user': 'xxxx@example.com'},
                      organization=self.organization,
                      template=TemplateFactory(email_required=True),
                      request=self.request)
        form = RequestForm(**kwargs)
        self.assertFalse(form.is_valid())

        kwargs['data']['body'] = kwargs['data']['email_user']
        form = RequestForm(**kwargs)
        self.assertTrue(form.is_valid())
