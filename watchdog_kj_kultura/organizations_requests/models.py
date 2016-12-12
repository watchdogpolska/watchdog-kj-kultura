from autoslug.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from ..organizations.models import Organization
from .fields import RelativeDeltaField
from .utils import parse_relativedelta_text

SHORTCODE_HELPTEXT = _("Supported is some shortcodes. Refer to the documentation.")
EMAIL_HELP_TEXT = _("E-mail is necessary for security purposes, " +
                    "as well as notification of the request.")


class TemplateQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Template(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    subject = models.CharField(verbose_name=_("Subject"), max_length=100)
    body = models.TextField(verbose_name=_("Body"))
    introduction = models.TextField(verbose_name=_("Introduction"), blank=True)
    email_required = models.BooleanField(blank=True,
                                         verbose_name=_("Require email"),
                                         help_text=_("Mark to require email in content of request"))
    visible = models.BooleanField(default=True,
                                  verbose_name=_("Public visible"),
                                  help_text=_("Check to mark template as public visible"))
    objects = TemplateQuerySet.as_manager()

    class Meta:
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")
        ordering = ['created', ]

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Notification(TimeStampedModel):
    template = models.ForeignKey(to=Template, verbose_name=_("Template"))
    delta = RelativeDeltaField(max_length=50,
                               verbose_name=_("The period for sending notification"))
    subject = models.CharField(max_length=100,
                               verbose_name=_("Subject of notification"),
                               help_text=SHORTCODE_HELPTEXT)
    body = models.TextField(verbose_name=_("Body of notification"),
                            help_text=SHORTCODE_HELPTEXT)

    def get_relativedelta(self):
        return parse_relativedelta_text(self.delta)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notification")
        ordering = ['template_id', ]


class RequestQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Request(TimeStampedModel):
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"))
    template = models.ForeignKey(Template, verbose_name=_("Used templates"))
    subject = models.CharField(verbose_name=_("Subject"), max_length=50)
    email = models.EmailField(verbose_name=_("Email of organization"))
    email_user = models.EmailField(verbose_name=_("E-mail"), help_text=EMAIL_HELP_TEXT)
    body = models.TextField(verbose_name=_("Content of the request"))
    objects = RequestQuerySet.as_manager()

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")
        ordering = ['created', ]

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('organizations_requests:details', kwargs={'pk': str(self.pk)})


class Event(TimeStampedModel):
    notification = models.ForeignKey(Notification, verbose_name=_("Notification"))
    request = models.ForeignKey(Request, verbose_name=_("Request"))
