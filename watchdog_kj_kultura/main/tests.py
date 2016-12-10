from django.test import TestCase

from ..users.factories import UserFactory
from ..users.models import User
from .templatetags.main_tags import (object_list_to_url_edit_obj,
                                     object_to_url_edit_obj)


class TempleTagsTestCase(TestCase):

    def test_object_to_url_edit_obj(self):
        obj = UserFactory()
        self.assertEqual(object_to_url_edit_obj(obj), '/admin/users/user/%s/change/' % (obj.pk))

    def test_object_list_to_url_edit_obj(self):
        qs = User.objects.all()
        self.assertEqual(object_list_to_url_edit_obj(qs), '/admin/users/user/')
