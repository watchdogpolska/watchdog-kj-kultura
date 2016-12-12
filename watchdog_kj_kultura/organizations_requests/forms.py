from atom.ext.crispy_forms.forms import SingleButtonMixin
from braces.forms import UserKwargModelFormMixin
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Request
from .emails import RequestOrganizationEmail, RequestUserEmail


class RequestForm(UserKwargModelFormMixin, SingleButtonMixin, forms.ModelForm):
    action_text = _("Send and save!")

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        self.template = kwargs.pop('template')
        self.request = kwargs.pop('request')
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['subject'].disabled = True
        self.fields['subject'].initial = self.template.subject
        self.fields['body'].initial = self.template.body
        self.fields['email'].disabled = True
        self.fields['email'].initial = self.organization.email
        if self.template.email_required:
            self.fields['body'].help_text = _("Your must enter your email address in " +
                                              " body of request.")

    def clean(self):
        cleaned_data = super(RequestForm, self).clean()
        email_user = cleaned_data.get("email_user")
        body = cleaned_data.get("body")

        if self.template.email_required and email_user not in body:
            msg = "Must put '{value}' in body for that template.".format(value=email_user)
            self.add_error('body', msg)

    def save(self, *args, **kwargs):
        self.instance.template = self.template
        self.instance.organization = self.organization
        super(RequestForm, self).save(*args, **kwargs)
        context = {'object': self.instance,
                   'url': self.request.build_absolute_uri(self.instance.get_absolute_url())}
        RequestOrganizationEmail().send(self.instance.organization.email, context)
        RequestUserEmail().send(self.instance.email_user, context)
        return self.instance

    class Meta:
        model = Request
        fields = ['subject', 'email', 'email_user', 'body']
