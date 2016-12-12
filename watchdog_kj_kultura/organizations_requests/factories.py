import factory
import factory.fuzzy

from ..organizations.factories import OrganizationFactory
from .models import Event, Notification, Request, Template


class TemplateFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Template-%d' % n)
    slug = factory.Sequence(lambda n: 'slug-%d' % n)
    subject = factory.fuzzy.FuzzyText()
    body = factory.fuzzy.FuzzyText()
    introduction = factory.fuzzy.FuzzyText()
    email_required = False

    class Meta:
        model = Template
        django_get_or_create = ('slug', )


class NotificationFactory(factory.django.DjangoModelFactory):
    template = factory.SubFactory(TemplateFactory)
    delta = factory.Sequence(lambda n: '%d days' % n)
    subject = factory.Sequence(lambda n: 'title-%d' % n)
    body = factory.fuzzy.FuzzyText()

    class Meta:
        model = Notification


class RequestFactory(factory.django.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)
    template = factory.SubFactory(TemplateFactory)
    subject = factory.Sequence(lambda n: 'Request-%d' % n)
    email = factory.LazyAttribute(lambda obj: obj.organization.email)
    email_user = factory.Sequence(lambda n: 'request-%d@example.com' % n)
    body = factory.fuzzy.FuzzyText()

    class Meta:
        model = Request


class EventFactory(factory.django.DjangoModelFactory):
    request = factory.SubFactory(RequestFactory)
    notification = factory.SubFactory(NotificationFactory)

    class Meta:
        model = Event
