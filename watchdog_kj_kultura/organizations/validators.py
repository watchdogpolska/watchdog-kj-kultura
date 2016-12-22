import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

ALLNUM_RE = re.compile('^[a-zA-Z0-9]+$')


def is_allnum(value):
    if ALLNUM_RE.match(value):
        return True
    raise ValidationError(
        _('%(value)s is not valid key. They are permitted only Latin characters and numbers.'),
        params={'value': value},
    )
