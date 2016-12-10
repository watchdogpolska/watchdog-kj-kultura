from autoslug.fields import AutoSlugField
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from teryt_tree.models import JednostkaAdministracyjna


class MetaCategoryQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class MetaCategory(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    key = models.CharField(verbose_name=_("Key"), max_length=25)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    objects = MetaCategoryQuerySet.as_manager()

    class Meta:
        verbose_name = _("MetaCategory")
        verbose_name_plural = _("MetaCategorys")
        ordering = ['pk', ]

    def __str__(self):
        return self.name


class OrganizationQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Organization(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    email = models.EmailField(verbose_name=_("E-mail"))
    jst = models.ForeignKey(JednostkaAdministracyjna)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    meta = JSONField(verbose_name=_("Metadata"), default={})
    objects = OrganizationQuerySet.as_manager()

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizations:details', kwargs={'slug': self.slug})
