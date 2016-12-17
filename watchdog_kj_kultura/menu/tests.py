from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.
from .validators import is_external_url, is_valid_url, is_external_or_valid_url


class ValidatorTestCase(TestCase):
    EXT_VALID = ['http://google.com/',
                 '://google.com',
                 'ftp://google.com']
    EXT_INVALID = ['http:/google.com',
                   'google.com',
                   '/google.com/']
    INT_VALID = ['/admin/']
    INT_INVALID = ['http://google/',
                   '/go',
                   '////']

    def test_is_external_url_for_valid_values(self):
        for value in self.EXT_VALID:
            self.assertTrue(is_external_url(value), msg=value)

    def test_is_external_url_for_invalid_values(self):
        for value in self.EXT_INVALID:
            self.assertFalse(is_external_url(value), msg=value)

    def test_is_valid_url_for_valid_values(self):
        for value in self.INT_VALID:
            self.assertTrue(is_valid_url(value), msg=value)

    def test_is_valid_url_for_invalid_values(self):
        for value in self.INT_INVALID:
            self.assertFalse(is_valid_url(value), msg=value)

    def test_is_external_or_valid_url_for_valid_values(self):
        for value in self.INT_VALID + self.EXT_VALID:
            is_external_or_valid_url(value)

    def test_is_external_or_valid_url_for_invalid_values(self):
        for value in ['xxxx', '//xxx/']:
            with self.assertRaises(ValidationError, msg=value):
                is_external_or_valid_url(value)
