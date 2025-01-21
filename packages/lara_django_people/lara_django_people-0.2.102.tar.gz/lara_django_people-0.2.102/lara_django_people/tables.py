"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people admin *

:details: lara_django_people admin module admin backend configuration.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - run "lara-django-dev tables_generator lara_django_people >> tables.py" to update this file
________________________________________________________________________
"""
# django Tests s. https://docs.djangoproject.com/en/4.1/topics/testing/overview/ for lara_django_people
# generated with django-extensions tests_generator  lara_django_people > tests.py (LARA-version)

import logging
import django_tables2 as tables


from .models import (
    ExtraData,
    EntityClass,
    Entity,
    EntityBankAccount,
    LaraUser,
    MeetingCalendar,
)

from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<img src="/media/{url}" height="48px", width="48px">', url=value
        )


class EditColumn(tables.Column):
    # add edit boostrap icon to column
    def render(self, value):
        return format_html(
            '<a href="/lara_django_people/entities/update/{url}"><i class="bi bi-pencil-square"></i></a>',
            url=value,
        )


class ExtraDataTable(tables.Table):
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:extradata-detail', [tables.A('pk')]))

    class Meta:
        model = ExtraData

        fields = (
            "data_type",
            "namespace",
            "uri",
            "data_json",
            "media_type",
            "iri",
            "url",
            "description",
            "file",
            "image",
            "office_room",
            "laboratory",
            "email",
        )


class EntityClassTable(tables.Table):
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:entityclass-detail', [tables.A('pk')]))

    class Meta:
        model = EntityClass

        fields = ("name", "description")


class EntityTable(tables.Table):
    # for simple datatables s.
    # https://github.com/fiduswriter/Simple-DataTables
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:entity-detail', [tables.A('pk')]))
    name_full = tables.Column(
        linkify=("lara_django_people:entity-details", [tables.A("pk")])
    )
    image = ImageColumn("image")
    # edit = tables.Column(
    #    linkify=('lara_django_people:entity-update',[{ "args": [tables.A('name_first')], "attrs":{ 'a': {'class': 'bi bi-pencil-square'}}}],   ) )

    edit = tables.Column(
        empty_values=(),
        verbose_name="Edit",
        default="Edit",
        linkify={
            "viewname": "lara_django_people:entity-update",
            "args": [(tables.A("pk"))],
        },
        attrs={"a": {"role": "button", "class": "inline-block rounded bg-red-500 text-neutral-50 hover:bg-red-600  focus:bg-red-800  active:bg-red-700  px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal transition duration-150 ease-in-out focus:outline-none focus:ring-0"}},
    )

    delete = tables.Column(
        empty_values=(),
        verbose_name="Delete",
        default="Delete",
        linkify={
            "viewname": "lara_django_people:entity-delete",
            "args": [(tables.A("pk"))],
        },
        attrs={"a": {"class": "btn btn-danger btn-sm"}},
    )

    selection = tables.CheckBoxColumn(
        empty_values=(),
        attrs={"name": "Select", "id": "check-all"},
        accessor="pk",
        orderable=False,
        verbose_name="Selected",
    )

    # edit = tables.Column(empty_values=(), verbose_name='Edit', default="Edit",
    #                      linkify={'viewname':'lara_django_people:entity-update', 'args' : [(tables.A('pk'))] },
    #                       )

    # delete = tables.LinkColumn('lara_django_people:entity-delete', args=[tables.A('delete-id')], attrs={
    # 'a': {'class': 'btn btn-danger'} })

    def render_acronym(self, value):
        return format_html(
            '<a href="/lara_django_people/entities/update/{url}">{url}</a>', url=value
        )

    def render_edit(self):
        return format_html('<i class="bi bi-pencil-square"></i>')

    def render_delete(self):
        return format_html('<i class="bi bi-trash"></i>')

    def render_selection(self, record):
        return mark_safe(
            f'<input type="checkbox" name="selected_rows" value="{record.pk}" class="row-checkbox">'
        )

    # def render_edit(self, record):
    #     return format_html(
    #         '<a href="/lara_django_people/entities/update/{url}"><i class="bi bi-pencil-square"></i></a>',
    #         url=record.pk
    #     )

    class Meta:
        model = Entity
        attrs = {"id": "entity-table"}
        template_name = "django_tables2/bootstrap4.html"

        fields = (
            "entity_class",
            "image",
            "name_full",
            "acronym",
            "affiliation_current",
            "email",
            "email_private",
            "email_permanent",
            "website",
            "phone_number_mobile",
            "phone_number_office",
            "phone_number_lab",
            "phone_number_home",
            "edit",
            "delete",
            "selection",
        )


class EntityBankAccountTable(tables.Table):
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:entitybankaccount-detail', [tables.A('pk')]))

    class Meta:
        model = EntityBankAccount

        fields = ("name_account", "account_no", "iban", "bic", "bank", "description")


class LaraUserTable(tables.Table):
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:larauser-detail', [tables.A('pk')]))
    user = tables.Column(
        linkify=("lara_django_people:lara-user-details", [tables.A("pk")])
    )

    class Meta:
        model = LaraUser

        fields = (
            "entity",
            "user",
            "welcome_screen_layout",
            "access_token",
            "access_control",
            "confirmation_token",
            "email_confirmed",
            "email_recover",
            "max_logins",
            "failed_logins",
            "ip_curr_login",
            "ip_last_login",
            "datetime_confirmed",
            "datetime_confirmation_sent",
        )


class MeetingsCalendarTable(tables.Table):
    # adding link to column <column-to-be-linked>
    # <column-to-be-linked> = tables.Column(linkify=('lara_django_people:meetingscalendar-detail', [tables.A('pk')]))

    class Meta:
        model = MeetingCalendar

        fields = (
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
            "last_modified",
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
        )
