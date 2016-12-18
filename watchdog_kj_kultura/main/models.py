from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from tinymce.models import HTMLField
from django.contrib.sites.models import Site


class SettingsQuerySet(models.QuerySet):
    pass


class Settings(TimeStampedModel):
    site = models.OneToOneField(Site, verbose_name=_("Site"))
    home_content = HTMLField(verbose_name=_("Content of home page"))
    objects = SettingsQuerySet.as_manager()

    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")
        ordering = ['created', ]
