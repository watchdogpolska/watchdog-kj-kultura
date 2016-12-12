from atom.ext.crispy_forms.forms import SingleButtonMixin
from crispy_forms.layout import Fieldset, Layout
from django import forms
from django.utils.translation import ugettext_lazy as _

from ..users.models import User
from .emails import OrganizationFixEmail
from .models import MetaCategory, Organization


class OrganizationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationAdminForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.meta = {category.key: self.cleaned_data['meta_%d' % (category.pk)]
                              for category in self.categories}
        return super(OrganizationAdminForm, self).save(*args, **kwargs)


class OrganizationFixForm(SingleButtonMixin, forms.ModelForm):
    sources = forms.CharField(widget=forms.Textarea(),
                              label=_("Sources of information"),
                              help_text=_("Write about where to get this information " +
                                          "so we can verify it."))
    worker = forms.BooleanField(label=_("I am working in this institution"),
                                help_text=_("Mark, if you work in this institution."),
                                required=False)

    def get_field_kwargs_for_category(self, category):
        kwargs = dict(label=category.name, required=False)
        if self.instance.meta:
            kwargs.update(dict(initial=self.instance.meta.get(category.key, ''),
                               required=False))
        return kwargs

    def get_field_for_category(self, *args, **kwargs):
        return forms.CharField(**self.get_field_kwargs_for_category(*args, **kwargs))

    def __init__(self, *args, **kwargs):
        super(OrganizationFixForm, self).__init__(*args, **kwargs)
        self.categories = MetaCategory.objects.all()

        self.meta_fields = {'meta_%d' % (category.pk): self.get_field_for_category(category)
                            for category in self.categories}
        self.fields.update(self.meta_fields)
        self.helper.layout = Layout(
            Fieldset(
                _('Basic data'),
                'name', 'email', 'jst', 'pos', 'category'
            ),
            Fieldset(
                _('Metadatas'),
                *self.meta_fields.keys()
            ),
            Fieldset(
                _('Verification'),
                'sources',
                'worker'
            ),

        )

    def get_recipients(self):
        return [x.email for x in User.objects.filter(notify_about_fix=True).all()]

    def save(self, *args, **kwargs):
        obj = super(OrganizationFixForm, self).save(commit=False)
        for category in self.categories:
            obj.meta[category.key] = self.cleaned_data['meta_%d' % (category.pk)]
        to = self.get_recipients()
        if to:
            OrganizationFixEmail().send(to, {'object': obj, 'sources': self.cleaned_data['sources'],
                                                            'worker': self.cleaned_data['worker']})
        return obj

    class Meta:
        model = Organization
        fields = ['name', 'email', 'jst', 'pos', 'category']

