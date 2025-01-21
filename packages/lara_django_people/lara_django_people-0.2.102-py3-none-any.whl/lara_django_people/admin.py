"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people admin *

:details: lara_django_people admin module admin backend configuration.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - run "lara-django-dev admin_generator lara_django_people >> admin.py" to update this file
________________________________________________________________________
"""

# -*- coding: utf-8 -*-
from django.contrib import admin


# from .forms import UserAdminChangeForm
# from .forms import UserAdminCreationForm

# if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
#     # Force the `admin` sign in process to go through the `django-allauth` workflow:
#     # https://docs.allauth.org/en/latest/common/admin.html#admin
#     admin.autodiscover()
#     admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


from .models import (
    ExtraData,
    EntityClass,
    EntityRole,
    Entity,
    EntityBankAccount,
    Group,
    LaraUser,
    MeetingCalendar,
)


@admin.register(ExtraData)
class ExtraDataAdmin(admin.ModelAdmin):
    list_display = (
        "data_type",
        "namespace",
        "media_type",
        "iri",
        "url",
        "description",
        "extradata_id",
        "file",
        "image",
        "office_room",
        "laboratory",
        "email",
    )
    list_filter = (
        "data_type",
        "namespace",
        "media_type",
        "office_room",
        "laboratory",
    )


@admin.register(EntityClass)
class EntityClassAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "entityclass_id")
    search_fields = ("name",)


@admin.register(EntityRole)
class EntityRoleAdmin(admin.ModelAdmin):
    list_display = ("entityrole_id", "name", "description")


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = (
        "name_full",
        "slug",
        "entity_class",
        "gender",
        "title",
        "name_first",
        "names_middle",
        "name_last",
        "names_last_previous",
        "name_nick",
        "acronym",
       
        "url",
        "orcid",
        "ror",
        "office_room",
        "laboratory",
        "email",
        "website",
        "phone_number_mobile",
        "phone_number_office",
        "phone_number_lab",
        "phone_number_home",
        "image",
        "entity_id",
    )
    list_filter = (
        "entity_class",
        "title",
       
        "affiliation_current",
        "affiliation_start",
        "affiliation_end",
        "office_room",
        "laboratory",
        "address",
        "date_birth",
        "date_death",
    )
    raw_id_fields = (
        "bank_accounts",
        "expertise",
        "interests",
        "work_topics",
        "affiliation_previous",
        "data_extra",
    )
    search_fields = ("slug",)


@admin.register(EntityBankAccount)
class EntityBankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "entitybankaccount_id",
        "name_account",
        "account_no",
        "iban",
        "bic",
        "bank",
        "description",
    )
    list_filter = ("bank",)
    raw_id_fields = ("data_extra",)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(LaraUser)
class LaraUserAdmin(admin.ModelAdmin):
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm
    list_display = (
        "username",
        "entity",
        "email_confirmed",
        "email_recover",
        "max_logins",
        "failed_logins",
        "ip_curr_login",
        "ip_last_login",
        "datetime_confirmed",
        "datetime_confirmation_sent",
    )
    list_filter = (
        "username",
        "entity",
        "datetime_confirmed",
        "datetime_confirmation_sent",
    )


@admin.register(MeetingCalendar)
class MeetingsCalendarAdmin(admin.ModelAdmin):
    list_display = (
        "name_display",
        "calendar_url",
        "summary",
        "description",
        "color",
        "ics",
        "datetime_start",
        "datetime_end",
        "duration",
        "all_day",
        "created",
        "datetime_last_modified",
        "timestamp",
        "location",
        "geolocation",
        "conference_url",
        "range",
        "related",
        "role",
        "tzid",
        "offset_utc",
        "alarm_repeat_json",
        "event_repeat",
        "event_repeat_json",
        "organiser",
        "meetingcalendar_id",
    )
    list_filter = (
        "datetime_start",
        "datetime_end",
        "all_day",
        "created",
        "datetime_last_modified",
        "timestamp",
        "location",
        "geolocation",
        "organiser",
    )
    raw_id_fields = ("tags", "attendees")
