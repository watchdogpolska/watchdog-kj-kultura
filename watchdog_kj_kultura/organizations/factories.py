import factory
import factory.fuzzy
from teryt_tree.factories import JednostkaAdministracyjnaFactory

from ..users.factories import UserFactory
from .models import Category, MetaCategory, Organization


class MetaCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'user%d' % n)
    key = factory.LazyAttribute(lambda obj: 'key_%s' % obj.name)

    class Meta:
        model = MetaCategory
        django_get_or_create = ('key', )


class OrganizationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Organization-%d' % n)
    slug = factory.LazyAttribute(lambda obj: 'slug-%s' % obj.name)
    email = factory.LazyAttribute(lambda obj: 'org-%s@example.com' % obj.name)
    user = factory.SubFactory(UserFactory)
    jst = factory.SubFactory(JednostkaAdministracyjnaFactory)
    visible = True

    class Meta:
        model = Organization
        django_get_or_create = ('slug', )


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Category-%d' % n)
    slug = factory.LazyAttribute(lambda obj: 'slug-%s' % obj.name)

    class Meta:
        model = Category
        django_get_or_create = ('slug', )
