"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_myproj gRPC handlers*

:details: lara_django_myproj gRPC handlers.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""

# generated with django-socio-grpc generateprpcinterface lara_django_people  (LARA-version)

#import logging
from django_socio_grpc.services.app_handler_registry import AppHandlerRegistry
from lara_django_people.grpc.services import ExtraDataService, EntityClassService, EntityRoleService, EntityService, EntityBankAccountService, GroupService, LaraUserService, MeetingsCalendarService

def grpc_handlers(server):
    app_registry = AppHandlerRegistry("lara_django_people", server)

    app_registry.get_grpc_module = lambda: "lara_django_people_grpc.v1"

    app_registry.register(ExtraDataService)

    app_registry.register(EntityClassService)

    app_registry.register(EntityRoleService)

    app_registry.register(EntityService)

    app_registry.register(EntityBankAccountService)

    app_registry.register(GroupService)

    app_registry.register(LaraUserService)

    app_registry.register(MeetingsCalendarService)
