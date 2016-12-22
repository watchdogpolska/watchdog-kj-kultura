import logging

from import_export import fields, resources

from .models import MetaCategory, Organization

logger = logging.getLogger(__name__)


class MetaField(fields.Field):

    def save(self, obj, data):
        if not self.readonly:
            obj.meta[self.attribute] = self.clean(data)

    def get_value(self, obj):
        return obj.meta[self.attribute]


class PositionField(fields.Field):

    def __init__(self, kind, *args, **kwargs):
        self.kind = kind
        super(PositionField, self).__init__(*args, **kwargs)

    def clean(self, data):
        value = super(PositionField, self).clean(data)
        try:
            return float(value)
        except ValueError as e:
            raise ValueError("Column '%s': %s" % (self.column_name, e))

    def save(self, obj, data):
        if not self.readonly:
            pos = getattr(obj, self.attribute)
            setattr(pos, self.kind, self.clean(data))

    def get_value(self, obj):
        pos = getattr(obj, self.attribute)
        return getattr(pos, self.kind)


class OrganizationResource(resources.ModelResource):
    lat = PositionField(kind='x', attribute='pos', column_name='pos[lat]')
    lng = PositionField(kind='y', attribute='pos', column_name='pos[lng]')

    def __init__(self, *args, **kwargs):
        super(OrganizationResource, self).__init__(*args, **kwargs)
        self.add_meta_fields()

    def get_meta_fields_kwargs(self, metacategory):
        return dict(column_name='meta[%s]' % (metacategory.key),
                    attribute=metacategory.key)

    def get_meta_fields(self, metacategory):
        return MetaField(**self.get_meta_fields_kwargs(metacategory))

    def add_meta_fields(self):
        for metacategory in MetaCategory.objects.all():
            self.fields['meta_%s' % (metacategory.key)] = self.get_meta_fields(metacategory)

    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'email', 'jst', 'user', 'category', 'visible')
        export_order = fields
