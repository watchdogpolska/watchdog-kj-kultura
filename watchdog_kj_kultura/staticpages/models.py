import os

from autoslug.fields import AutoSlugField
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
from django.utils.functional import cached_property


class PageQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Page(MPTTModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    parent = TreeForeignKey('self', verbose_name=_("Parent"),
                            null=True,
                            blank=True,
                            related_name='children',
                            db_index=True)
    objects = PageQuerySet.as_manager()
    content = HTMLField(verbose_name=_("Content"))
    visible = models.BooleanField(verbose_name=_("Public visible"),
                                  help_text=_("Check to mark page as public visible"),
                                  default=False)
    # Field as in TimeStampedModel
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    def use_map(self):
        return '[map]' in self.content
    use_map.short_description = _('Use map?')
    use_map.boolean = True

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('staticpages:details', kwargs={'slug': self.slug})


class AttachmentQuerySet(models.QuerySet):
    pass


@python_2_unicode_compatible
class Attachment(TimeStampedModel):
    file = models.FileField(_("File"))
    objects = AttachmentQuerySet.as_manager()

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
        ordering = ['created', ]

    @cached_property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.filename

    def get_absolute_url(self):
        return reverse('staticpages:details', kwargs={'slug': self.slug})
