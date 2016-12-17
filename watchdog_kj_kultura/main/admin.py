from django.contrib import admin
from .models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    '''
        Admin View for Settings
    '''
    list_display = ('site', 'created', 'modified')
