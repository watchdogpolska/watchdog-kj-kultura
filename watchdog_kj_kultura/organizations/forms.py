from django import forms


class OrganizationAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationAdminForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.meta = {category.key: self.cleaned_data['meta_%d' % (category.pk)]
                              for category in self.categories}
        return super(OrganizationAdminForm, self).save(*args, **kwargs)
