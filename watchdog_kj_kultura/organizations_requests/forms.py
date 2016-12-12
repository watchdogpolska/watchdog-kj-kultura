from atom.ext.crispy_forms.forms import SingleButtonMixin
from django import forms
from django.utils.translation import ugettext_lazy as _


def contains_email_validator(content):
    return False


class OrganizationRequestForm(SingleButtonMixin, forms.Form):
    subject = forms.CharField(label=_("Subject"), disabled=True)
    email = forms.CharField(label=_("E-mail address"), disabled=True)
    body = forms.CharField(label=_("Content of the request"),
                           validators=[contains_email_validator],
                           widget=forms.Textarea())
    action_text = _("Send requests")

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        super(OrganizationRequestForm, self).__init__(*args, **kwargs)

    def save(self):
        pass
        return self.instance

    class Meta:
        fields = []
