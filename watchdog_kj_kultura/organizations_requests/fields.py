from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from .validators import is_valid_relative_date


PERIOD_HELP_TEXT = _("Try to write words a period of time.")


class RelativeDeltaField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', PERIOD_HELP_TEXT)
        super(RelativeDeltaField, self).__init__(*args, **kwargs)
        self.validators.append(is_valid_relative_date)
