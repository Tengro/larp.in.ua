from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy

from larp_in_ua.apps.accounts.models import UserAccount
from larp_in_ua.apps.scheduler.models import EventRegistration


admin.site.unregister(Group)


class EventRegistrationUserInline(admin.StackedInline):
    model = EventRegistration
    fields = ['__str__', 'event', 'registration_status']
    readonly_fields = ['__str__', ]


@admin.register(UserAccount)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (gettext_lazy("Personal info"), {"fields": ("email", "first_name", "last_name", "telegram_id")}),
        (
            gettext_lazy("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions", "is_tengro")},
        ),
        (gettext_lazy("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    readonly_fields = ("email",)
    inlines = [EventRegistrationUserInline, ]
