from django.contrib import admin
from larp_in_ua.apps.scheduler.models import Event, EventRegistration


class EventRegistrationUserInline(admin.StackedInline):
    model = EventRegistration
    fields = ['__str__', 'user', 'registration_status', '_times_asked']
    readonly_fields = ['__str__', ]


# Register your models here.
@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ("event_time", "title", "event_type", "event_lane", 'organizers',)
    search_fields = ("title", "organizers", "email")
    inlines = [EventRegistrationUserInline, ]
