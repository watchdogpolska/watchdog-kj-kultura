from datetime import timedelta

from django.core import mail, management
from django.test import TestCase
from django.utils.timezone import now

from ..factories import NotificationFactory, RequestFactory
from ..models import Event

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class NotificationCommandsTestCase(TestCase):

    def setUp(self):
        self.notification = NotificationFactory(delta="3 day")
        # event in 2 and 4 days from now
        self.request_should_trigger = RequestFactory(template=self.notification.template,
                                                     created=now() - timedelta(days=4))
        self.request_should_not_trigger = RequestFactory(template=self.notification.template,
                                                         created=now() - timedelta(days=2))
        self.stdout = StringIO()

    def test_triggering_reminders(self):
        management.call_command('send_requests_notifications', stdout=self.stdout)

        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.get()
        self.assertEqual(event.request, self.request_should_trigger)
        self.assertEqual(event.notification, self.notification)

    def test_double_run_command(self):
        management.call_command('send_requests_notifications', stdout=self.stdout)
        self.assertEqual(Event.objects.count(), 1)
        management.call_command('send_requests_notifications', stdout=self.stdout)
        self.assertEqual(Event.objects.count(), 1)

    def test_send_email(self):
        management.call_command('send_requests_notifications', stdout=self.stdout)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox.pop()
        self.assertIn(self.request_should_trigger.email_user, msg.to)

    def test_output_contains_requests_title(self):
        management.call_command('send_requests_notifications', stdout=self.stdout)
        content = self.stdout.getvalue()
        self.assertIn(self.request_should_trigger.email_user, content)

    def test_output_contains_counter(self):
        management.call_command('send_requests_notifications', stdout=self.stdout)
        content = self.stdout.getvalue()
        self.assertIn("1 notifications was send!", content)
