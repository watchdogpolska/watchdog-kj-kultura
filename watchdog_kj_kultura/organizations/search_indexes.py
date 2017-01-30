from haystack import indexes
from .models import Organization


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField()
    category = indexes.CharField(model_attr='category__slug')
    created = indexes.DateTimeField()
    modified = indexes.DateTimeField()
    jst = indexes.FacetCharField(model_attr='jst__slug')

    def prepare_jst(self, obj):
        if self.jst:
            return obj.jst.slug
        return None

    def get_model(self):
        return Organization

    def get_updated_field(sef):
        return 'modified'

    def index_queryset(self, using=None):
        return self.get_model().objects.select_related('category', 'jst').visible().all()
