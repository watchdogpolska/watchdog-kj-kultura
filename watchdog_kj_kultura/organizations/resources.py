import logging

from functools import lru_cache
from import_export import fields, resources

from ..teryt.models import JednostkaAdministracyjna
from .models import MetaCategory, Organization

logger = logging.getLogger(__name__)


class MetaField(fields.Field):

    def save(self, obj, data):
        if not self.readonly:
            obj.meta[self.attribute] = self.clean(data)

    def get_value(self, obj):
        try:
            return obj.meta[self.attribute]
        except KeyError:
            return None


@lru_cache(maxsize=150)
def get_jst(pk):
    return JednostkaAdministracyjna.objects.get(pk=pk)


class JSTField(fields.Field):
    def clean(self, data):
        pk = data[self.column_name].rjust(7, '0')
        try:
            return get_jst(pk)
        except JednostkaAdministracyjna.DoesNotExist:
            return None


class PositionField(fields.Field):
    fields = ['x', 'y']

    def __init__(self, kind, *args, **kwargs):
        self.kind = kind
        super(PositionField, self).__init__(*args, **kwargs)

    def clean(self, data):
        value = super(PositionField, self).clean(data)
        if value:
            try:
                return float(value)
            except ValueError as e:
                raise ValueError("Column '%s': %s" % (self.column_name, e))

    def save(self, obj, data):
        if not self.readonly:
            pos = getattr(obj, self.attribute)
            if not pos:
                pos = {'type': 'Point', 'coordinates': [0, 0]}
            pos['coordinates'][self.fields.index(self.kind)] = self.clean(data)

    def get_value(self, obj):
        pos = getattr(obj, self.attribute)
        if not pos:
            return None
        return pos['coordinates'][self.fields.index(self.kind)]


class OrganizationResource(resources.ModelResource):
    lat = PositionField(kind='x', attribute='pos', column_name='pos[lat]')
    lng = PositionField(kind='y', attribute='pos', column_name='pos[lng]')
    jst = JSTField(attribute='jst', column_name='jst')

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
        fields = ('id', 'name', 'slug', 'email', 'user', 'category', 'visible')
        export_order = fields
