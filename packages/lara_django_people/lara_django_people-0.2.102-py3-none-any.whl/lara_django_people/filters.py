"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people filter app *

:details: lara_django_people filter app. 
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

from django_filters.rest_framework import FilterSet, CharFilter, DateRangeFilter

from .models import Entity, EntityClass, EntityRole, Group, LaraUser, MeetingCalendar


class EntityFilterSet(FilterSet):
    class Meta:
        model = Entity
        fields = {
            "slug": ["exact", "contains"],
            "gender": ["exact"],
            "title": ["exact", "contains"],
            "name_first": ["exact", "contains"],
            "name_last": ["exact", "contains"],
            "names_middle": ["exact", "contains"],
            "name_full": ["exact", "contains"],
            "name_nick": ["exact", "contains"],
            "names_last_previous": ["exact", "contains"],
            "acronym": ["exact", "contains"],
            "url": ["exact", "contains"],
            "pid": ["exact", "contains"],
            "iri": ["exact", "contains"],
            "orcid": ["exact", "contains"],
            "barcode": ["exact", "contains"],
            "tax_no": ["exact", "contains"],
            "vat_no": ["exact", "contains"],
            "toll_no": ["exact", "contains"],
            "email": ["exact", "contains"],
            "email_private": ["exact", "contains"],
            "email_permanent": ["exact", "contains"],
            "website": ["exact", "contains"],
            "phone_number_mobile": ["exact", "contains"],
            "phone_number_office": ["exact", "contains"],
            "phone_number_lab": ["exact", "contains"],
            "phone_number_home": ["exact", "contains"],
            "date_birth": ["exact", "contains", "gte", "lte"],
            "date_death": ["exact", "contains", "gte", "lte"],
            "datetime_last_modified": ["exact", "contains", "gte", "lte"],
            "remarks": ["exact", "contains"],
        }


class EntityClassFilterSet(FilterSet):
    class Meta:
        model = EntityClass
        fields = {
            "name": ["exact", "contains"],
            "description": ["exact", "contains"],
        }


class EntityRoleFilterSet(FilterSet):
    class Meta:
        model = EntityRole
        fields = {
            "name": ["exact", "contains"],
            "description": ["exact", "contains"],
        }


class GroupFilterSet(FilterSet):
    class Meta:
        model = Group
        fields = {
            "name": ["exact", "contains"],
            "name_full": ["exact", "contains"],
            "remarks": ["exact", "contains"],
            "description": ["exact", "contains"],
        }


class MeetingsCalendarFilterSet(FilterSet):
    class Meta:
        model = MeetingCalendar
        fields = {
            "name_display": ["exact", "contains"],
            "summary": ["exact", "contains"],
            "datetime_start": ["exact", "contains", "gte", "lte"],
            "datetime_end": ["exact", "contains", "gte", "lte"],
            "all_day": ["exact"],
            "related": ["exact"],
            "tzid": ["exact"],
            "offset_utc": ["exact", "lte", "gte"],
            "description": ["exact", "contains"],
        }
