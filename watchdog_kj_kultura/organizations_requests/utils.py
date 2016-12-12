import re

from dateutil.relativedelta import relativedelta
from .exceptions import RelativeDateParseException

DELTA_REGEXP = ('(?:(?P<year>\d+) years{0,1}){0,1}\s*' +
                '(?:(?P<month>\d+) months{0,1}){0,1}\s*' +
                '(?:(?P<day>\d+) days{0,1}){0,1}\s*' +
                '(?:(?P<hour>\d+) hour{0,1}){0,1}\s*')


def parse_relativedelta_text(text):
    match = re.match(DELTA_REGEXP, text.strip())
    if not match or all(x is None for x in match.groups()):
        raise RelativeDateParseException("Unable to parse '%s' date string" % (text))
    return relativedelta(month=int(match.group('month') or 0),
                         days=int(match.group('day') or 0),
                         hour=int(match.group('hour') or 0))
