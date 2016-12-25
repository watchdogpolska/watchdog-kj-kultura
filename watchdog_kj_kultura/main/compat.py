try:
    from django.apps import apps  # noqa

    def get_model(app_label, model_name):
        return apps.get_model(app_label, model_name)
except ImportError:  # Django <1.9
    from django.db.models import get_model  # noqa
