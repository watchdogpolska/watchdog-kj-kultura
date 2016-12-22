from django.test import TestCase
from ..validators import is_allnum
from django.core.exceptions import ValidationError


class ValidatorTestCase(TestCase):

    def test_is_allnum_valid(self):
        CASE = ['x', '12', '123xx']
        for value in CASE:
            self.assertTrue(is_allnum(value))

    def test_is_allnum_invalid(self):
        CASE = ['15 xxx', '123xłś', 'xxx ', '15.5']
        for value in CASE:
            with self.assertRaises(ValidationError):
                is_allnum(value)
