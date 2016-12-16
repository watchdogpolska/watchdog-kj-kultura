from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Attachment, Page


@admin.register(Page)
class PageAdmin(MPTTModelAdmin):
    '''
        Admin View for Page
    '''
    list_display = ('name', 'created', 'modified', 'user', 'use_map', 'visible')
    list_filter = ('created', 'modified', 'user')
    search_fields = ('name', 'content')

    class Media:
        js = ('watchdog_filebrowser/js/attachment_init.js',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    '''
        Admin View for Attachment
    '''
    list_display = ('pk', 'filename')
    list_filter = ('created', 'modified')
    search_fields = ('file',)
