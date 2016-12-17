from haystack import indexes
from .models import Organization


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField()
    created = indexes.DateTimeField()
    modified = indexes.DateTimeField()

    def get_model(self):
        return Organization

    def get_updated_field(sef):
        return 'modified'

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(visible=True)
