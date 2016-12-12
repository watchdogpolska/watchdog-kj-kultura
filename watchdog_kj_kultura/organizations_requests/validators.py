from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .exceptions import RelativeDateParseException
from .utils import parse_relativedelta_text


def is_valid_relative_date(value):
    try:
        parse_relativedelta_text(value)
        return True
    except RelativeDateParseException:
        raise ValidationError(
            _('%(value)s is not valid delta data'),
            params={'value': value},
        )
