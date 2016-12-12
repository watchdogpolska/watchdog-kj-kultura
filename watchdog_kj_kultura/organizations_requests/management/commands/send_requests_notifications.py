from django.core.management import BaseCommand
from ...models import Request, Notification, Event
from ...emails import RequestNotificationEmail
from django.utils.timezone import now


class Command(BaseCommand):
    help = "Command to create and send notification to remind user about the request."
    email = RequestNotificationEmail()

    def handle_new_notification(self, notification, request):
        deadline = request.created + notification.get_relativedelta()
        self.email.send(request.email_user, {'notification': notification,
                                             'request': request,
                                             'deadline': deadline})
        Event.objects.create(notification=notification,
                             request=request)
        self.stdout.write("Send notification {notification} to {email} about {request}".
                          format(notification=notification,
                                 email=request.email_user,
                                 request=request))

    def handle(self, *args, **options):
        count = 0
        for notification in Notification.objects.select_related('template').all():
            limit_date = now() - notification.get_relativedelta()
            requests = (Request.objects.filter(template=notification.template).
                        exclude(event__notification=notification).
                        filter(created__lte=limit_date).all())

            for request in requests:
                self.handle_new_notification(notification, request)
                count += 1
        self.stdout.write("{0} notifications was send!".format(count))
