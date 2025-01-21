"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_myproj gRPC services*

:details: lara_django_myproj gRPC services.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

## generated with django-socio-grpc generateprpcinterface lara_django_people  (LARA-version)

import io
import asyncio
import grpc
import logging

from asgiref.sync import sync_to_async
from django_socio_grpc.decorators import grpc_action

from django_socio_grpc import generics, mixins
from lara_django_base.grpc.mixins import AsyncUploadModelMixin, AsyncRetrieveByNameModelMixin, AsyncDownloadModelMixin


from .serializers import (
    ExtraDataProtoSerializer,
    EntityClassProtoSerializer,
    EntityRoleProtoSerializer,
    EntityProtoSerializer,
    EntityBankAccountProtoSerializer,
    GroupProtoSerializer,
    LaraUserProtoSerializer,
    MeetingsCalendarProtoSerializer,
)

from ..filters import EntityClassFilterSet, EntityRoleFilterSet, EntityFilterSet, GroupFilterSet, MeetingsCalendarFilterSet

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

logger = logging.getLogger(__name__)

class ExtraDataService(generics.AsyncModelService, mixins.AsyncStreamModelMixin, AsyncUploadModelMixin,
    AsyncRetrieveByNameModelMixin,
    AsyncDownloadModelMixin,):
    queryset = ExtraData.objects.all()
    serializer_class = ExtraDataProtoSerializer


class EntityClassService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = EntityClass.objects.all()
    serializer_class = EntityClassProtoSerializer
    filterset_class = EntityClassFilterSet

class EntityRoleService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = EntityRole.objects.all()
    serializer_class = EntityRoleProtoSerializer
    filterset_class = EntityRoleFilterSet

    
class EntityService(generics.AsyncModelService, mixins.AsyncStreamModelMixin, AsyncUploadModelMixin,
    AsyncRetrieveByNameModelMixin,
    AsyncDownloadModelMixin,):
    queryset = Entity.objects.all()
    serializer_class = EntityProtoSerializer
    filterset_class = EntityFilterSet


class GroupService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupProtoSerializer
    filterset_class = GroupFilterSet


class EntityBankAccountService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = EntityBankAccount.objects.all()
    serializer_class = EntityBankAccountProtoSerializer


class LaraUserService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = LaraUser.objects.all()
    serializer_class = LaraUserProtoSerializer


class MeetingsCalendarService(generics.AsyncModelService, mixins.AsyncStreamModelMixin):
    queryset = MeetingCalendar.objects.all()
    serializer_class = MeetingsCalendarProtoSerializer
    filterset_class = MeetingsCalendarFilterSet
