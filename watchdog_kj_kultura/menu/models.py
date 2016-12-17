from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from .validators import is_external_or_valid_url, is_external_url


class ElementQuerySet(models.QuerySet):
    def root_with_children(self, visible=True):
        qs = self
        qs_children = Element.objects.all()
        if visible is not None:
            qs = qs.filter(visible=visible)
            qs_children = qs_children.filter(visible=visible)
        return qs.prefetch('children', queryset=qs)

    def with_children_count(self):
        return self.annotate(children_count=models.Count('element'))


@python_2_unicode_compatible
class Element(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    url = models.CharField(verbose_name=_("URL"),
                           max_length=100,
                           validators=[is_external_or_valid_url])
    parent = models.ForeignKey(to='self',
                               verbose_name=_("Parent"),
                               null=True,
                               blank=True,
                               limit_choices_to={'parent': None})
    visible = models.BooleanField(verbose_name=_("Public visible"),
                                  help_text=_("Check to mark element as public visible"),
                                  default=False)
    position = models.SmallIntegerField(verbose_name=_("Position"), default=0)
    objects = ElementQuerySet.as_manager()

    class Meta:
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")
        ordering = ['position', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.url

    def is_external_url(self):
        return is_external_url(self.url)
    is_external_url.short_description = _('Is external URL?')
    is_external_url.boolean = True
