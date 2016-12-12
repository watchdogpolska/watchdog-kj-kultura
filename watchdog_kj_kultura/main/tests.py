from django.test import RequestFactory, TestCase
from django.views.generic import TemplateView

from ..users.factories import UserFactory
from ..users.models import User
from .templatetags.main_tags import (object_list_to_url_edit_obj,
                                     object_to_url_edit_obj)
from .views import BreadcrumbsMixin
from django.core.exceptions import ImproperlyConfigured


class TempleTagsTestCase(TestCase):

    def test_object_to_url_edit_obj(self):
        obj = UserFactory()
        self.assertEqual(object_to_url_edit_obj(obj), '/admin/users/user/%s/change/' % (obj.pk))

    def test_object_list_to_url_edit_obj(self):
        qs = User.objects.all()
        self.assertEqual(object_list_to_url_edit_obj(qs), '/admin/users/user/')


class BreadcrumbsMixinTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/customer/details')

    def test_raises_missing_breadcrumbs(self):
        class CustomView(BreadcrumbsMixin, TemplateView):
            pass
        with self.assertRaises(ImproperlyConfigured):
            CustomView.as_view()(self.request)
