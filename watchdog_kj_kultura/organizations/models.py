from autoslug.fields import AutoSlugField
from django.conf import settings
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
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


class CategoryQuerySet(models.QuerySet):

    def with_organization_count(self):
        return self.annotate(organization_count=models.Count('organization'))


@python_2_unicode_compatible
class Category(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizations:list', kwargs={'category': self.slug})


class OrganizationQuerySet(models.QuerySet):

    def area(self, jst):
        return self.filter(jst__tree_id=jst.tree_id,
                           jst__lft__range=(jst.lft, jst.rght))


@python_2_unicode_compatible
class Organization(TimeStampedModel):
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    slug = AutoSlugField(populate_from='name', verbose_name=_("Slug"), unique=True)
    email = models.EmailField(verbose_name=_("E-mail"))
    jst = models.ForeignKey(JednostkaAdministracyjna,
                            verbose_name=_("Unit of administrative division"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    pos = gismodels.PointField(verbose_name=_("Position"), null=True, blank=True, db_index=True)
    category = models.ForeignKey(to=Category,
                                 verbose_name=_("Category"),
                                 null=True,
                                 blank=True)
    meta = JSONField(verbose_name=_("Metadata"), default={})
    objects = OrganizationQuerySet.as_manager()

    def geocode_input(self):
        if self.pos:
            return "{0}, {1}".format(self.pos.coords[1], self.pos.coords[0])
        return self.name or "Warszawa, mazowieckie, Polska"

    def set_geopy_point(self, point):
        self.pos = Point(point.point.longitude, point.point.latitude)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ['created', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizations:details', kwargs={'slug': self.slug})

    @property
    def absolute_url(self):
        return self.get_absolute_url()
