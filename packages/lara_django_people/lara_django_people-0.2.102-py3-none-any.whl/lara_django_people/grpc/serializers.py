"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_myproj gRPC serializer*

:details: lara_django_myproj gRPC serializer.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

## generated with django-socio-grpc generateprpcinterface lara_django_people  (LARA-version)

import logging

from rest_framework.serializers import UUIDField, PrimaryKeyRelatedField, ImageField
from django_socio_grpc import proto_serializers


from django.contrib.auth.models import User

from lara_django_base.models import (
    Namespace,
    DataType,
    MediaType,
    Namespace,
    Tag,
    Room,
    Address,
    Location,
)
from lara_django_people.models import (
    ExtraData,
    EntityClass,
    EntityRole,
    Entity,
    EntityBankAccount,
    Group,
    LaraUser,
    MeetingCalendar,
)

import lara_django_people_grpc.v1.lara_django_people_pb2 as lara_django_people_pb2


class ExtraDataProtoSerializer(proto_serializers.ModelProtoSerializer):
    data_type = PrimaryKeyRelatedField(
        queryset=DataType.objects.all(), pk_field=UUIDField(format="hex_verbose"), required=False, allow_null=True
    )
    namespace = PrimaryKeyRelatedField(queryset=Namespace.objects.all(), pk_field=UUIDField(format="hex_verbose"))
    media_type = PrimaryKeyRelatedField(
        queryset=MediaType.objects.all(), pk_field=UUIDField(format="hex_verbose"), required=False, allow_null=True
    )

    class Meta:
        model = ExtraData
        proto_class = lara_django_people_pb2.ExtraDataResponse

        proto_class_list = lara_django_people_pb2.ExtraDataListResponse

        fields = "__all__"  # [data_type', namespace', URI', text', XML', JSON', bin', media_type', IRI', URL', description', file', image', office_room', laboratory', email']


class EntityClassProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = EntityClass
        proto_class = lara_django_people_pb2.EntityClassResponse

        proto_class_list = lara_django_people_pb2.EntityClassListResponse

        fields = "__all__"  # [name', description']


class EntityRoleProtoSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = EntityRole
        proto_class = lara_django_people_pb2.EntityRoleResponse

        proto_class_list = lara_django_people_pb2.EntityRoleListResponse

        fields = "__all__"  # [name', description']


class EntityProtoSerializer(proto_serializers.ModelProtoSerializer):
    entity_class = PrimaryKeyRelatedField(queryset=EntityClass.objects.all(), allow_null=True, required=False)
    bank_accounts = PrimaryKeyRelatedField(
        queryset=EntityBankAccount.objects.all(), allow_null=True, required=False, many=True
    )
    expertise = PrimaryKeyRelatedField(queryset=Tag.objects.all(), allow_null=True, required=False, many=True)
    interests = PrimaryKeyRelatedField(queryset=Tag.objects.all(), allow_null=True, required=False, many=True)
    work_topics = PrimaryKeyRelatedField(queryset=Tag.objects.all(), allow_null=True, required=False, many=True)
    roles = PrimaryKeyRelatedField(queryset=EntityRole.objects.all(), allow_null=True, required=False, many=True)
    affiliation_current = PrimaryKeyRelatedField(queryset=Entity.objects.all(), allow_null=True, required=False)
    affiliation_previous = PrimaryKeyRelatedField(
        queryset=Entity.objects.all(), allow_null=True, required=False, many=True
    )
    office_room = PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
    laboratory = PrimaryKeyRelatedField(queryset=Room.objects.all(), allow_null=True, required=False)
    address = PrimaryKeyRelatedField(queryset=Address.objects.all(), allow_null=True, required=False)

    data_extra = PrimaryKeyRelatedField(queryset=ExtraData.objects.all(), allow_null=True, required=False, many=True)

    # image = ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    class Meta:
        model = Entity
        proto_class = lara_django_people_pb2.EntityResponse

        proto_class_list = lara_django_people_pb2.EntityListResponse

        fields = "__all__"  # [slug', entity_class', gender', title', name_first', names_middle', name_last', name_full', names_last_previous', name_nick', acronym', URL', handle', IRI', orcid', ror', tax_no', vat_no', toll_no', affiliation_current', affiliation_start', affiliation_end', office_room', laboratory', email', email_private', email_permanent', website', phone_number_mobile', phone_number_office', phone_number_lab', phone_number_home', address', date_birth', date_death', color', icon', image']


class GroupProtoSerializer(proto_serializers.ModelProtoSerializer):
    namespace = PrimaryKeyRelatedField(queryset=Namespace.objects.all(), allow_null=True, required=False)
    group_class = PrimaryKeyRelatedField(queryset=EntityClass.objects.all(), allow_null=True, required=False)
    members = PrimaryKeyRelatedField(queryset=Entity.objects.all(), allow_null=True, required=False, many=True)

    class Meta:
        model = Group
        proto_class = lara_django_people_pb2.GroupResponse

        proto_class_list = lara_django_people_pb2.GroupListResponse

        fields = "__all__"  # [name', description']


class EntityBankAccountProtoSerializer(proto_serializers.ModelProtoSerializer):
    bank = PrimaryKeyRelatedField(queryset=Entity.objects.all(), allow_null=True, required=False)
    data_extra = PrimaryKeyRelatedField(queryset=ExtraData.objects.all(), allow_null=True, required=False, many=True)

    class Meta:
        model = EntityBankAccount
        proto_class = lara_django_people_pb2.EntityBankAccountResponse

        proto_class_list = lara_django_people_pb2.EntityBankAccountListResponse

        fields = "__all__"  # [name_account', account_no', iban', bic', bank', description']


class LaraUserProtoSerializer(proto_serializers.ModelProtoSerializer):
    entity = PrimaryKeyRelatedField(queryset=Entity.objects.all(), allow_null=True, required=False)
    

    class Meta:
        model = LaraUser
        proto_class = lara_django_people_pb2.LaraUserResponse

        proto_class_list = lara_django_people_pb2.LaraUserListResponse

        fields = "__all__"  # [entity', user', welcome_screen_layout', access_token', access_control', confirmation_token', email_confirmed', email_recover', max_logins', failed_logins', ip_curr_login', ip_last_login', datetime_confirmed', datetime_confirmation_sent']


class MeetingsCalendarProtoSerializer(proto_serializers.ModelProtoSerializer):
    organiser = PrimaryKeyRelatedField(queryset=LaraUser.objects.all(), allow_null=True, required=False)
    attendees = PrimaryKeyRelatedField(queryset=LaraUser.objects.all(), allow_null=True, required=False, many=True)

    class Meta:
        model = MeetingCalendar
        proto_class = lara_django_people_pb2.MeetingsCalendarResponse

        proto_class_list = lara_django_people_pb2.MeetingsCalendarListResponse

        fields = "__all__"  # [title', calendar_url', summary', description', color', ics', datetime_start', datetime_end', duration', all_day', created', last_modified', timestamp', location', geolocation', conference_url', range', related', role', tzid', offset_utc', alarm_repeat_json', event_repeat', event_repeat_json', organiser']
