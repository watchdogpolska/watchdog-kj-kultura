from django.contrib import admin

from .models import Event, Request, Notification, Template


class NotificationInline(admin.StackedInline):
    '''
    Stacked Inline View for Notification
    '''
    model = Notification


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    '''
    Admin View for Request
    '''
    list_display = ('name', 'subject', 'visible', 'email_required', 'created', 'modified')
    list_filter = ('created', 'visible')
    inlines = [
        NotificationInline,
    ]
    search_fields = ('subject',)


class EventInline(admin.StackedInline):
    '''
        Stacked Inline View for Event
    '''
    model = Event


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    '''
        Admin View for Request
    '''
    list_display = ('subject', 'email_user', 'organization', 'created', 'modified', )
    list_filter = ('created',)
    inlines = [
        EventInline,
    ]
    search_fields = ('subject', 'organization')
