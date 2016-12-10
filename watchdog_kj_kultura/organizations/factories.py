import factory
import factory.fuzzy

from .models import MetaCategory, Organization
from ..users.factories import UserFactory
from teryt_tree.factories import JednostkaAdministracyjnaFactory


class MetaCategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'user%d' % n)
    key = factory.LazyAttribute(lambda obj: 'key_%s' % obj.name)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = MetaCategory
        django_get_or_create = ('key', )


class OrganizationFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'Organization-%d' % n)
    slug = factory.LazyAttribute(lambda obj: 'slug-%s' % obj.name)
    user = factory.SubFactory(UserFactory)
    jst = factory.SubFactory(JednostkaAdministracyjnaFactory)

    class Meta:
        model = Organization
        django_get_or_create = ('slug', )
