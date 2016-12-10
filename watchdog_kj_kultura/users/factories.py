import factory
import factory.fuzzy
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.PostGenerationMethodCall('set_password', 'pass')

    class Meta:
        model = get_user_model()  # Equivalent to ``model = myapp.models.User``
        django_get_or_create = ('username', )
