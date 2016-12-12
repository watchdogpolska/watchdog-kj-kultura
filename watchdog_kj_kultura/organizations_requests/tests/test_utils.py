from dateutil.relativedelta import relativedelta
from unittest import TestCase
from ..utils import parse_relativedelta_text
from ..exceptions import RelativeDateParseException


class parse_relativedelta_textTestCase(TestCase):

    def test_valid_deltas(self):
        CASE = {'15 months 14 days 3 hour': relativedelta(month=15, days=14, hour=3),
                '15 month 14 days': relativedelta(month=15, days=14, hour=0),
                '3 months 4 hour': relativedelta(month=3, days=0, hour=4),
                }
        for value, expected in CASE.items():
            self.assertEqual(parse_relativedelta_text(value), expected)

    def test_raises_for_invalid(self):
        CASE = ['15 xxx', 'anakonda', 'Bogus BGC']
        for value in CASE:
            with self.assertRaises(RelativeDateParseException,
                                   msg="Missing exception for '%s'" % (value)):
                parse_relativedelta_text(value)
