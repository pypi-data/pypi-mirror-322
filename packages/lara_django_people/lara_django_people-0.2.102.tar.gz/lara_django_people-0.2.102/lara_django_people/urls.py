"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people urls *

:details: lara_django_people urls module.
         - add app specific urls here
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: -
________________________________________________________________________
"""

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django_socio_grpc.settings import grpc_settings

from . import views

# Add your {cookiecutter.project_slug}} urls here.


# !! this sets the apps namespace to be used in the template
app_name = "lara_django_people"

# companies and institutions should also be added
# the 'name' attribute is used in templates to address the url independent of the view

#     path('edit/', profile_edit_view, name="profile-edit"),
#     path('onboarding/', profile_edit_view, name="profile-onboarding"),
#     path('settings/', profile_settings_view, name="profile-settings"),
#     path('emailchange/', profile_emailchange, name="profile-emailchange"),
#     path('emailverify/', profile_emailverify, name="profile-emailverify"),
#     path('delete/', profile_delete_view, name="profile-delete"),


urlpatterns = [
    path('onboarding/', view=views.EntityCreateView.as_view(), name="profile-onboarding"),
#     path("~redirect/", view=views.lara_user_redirect_view, name="redirect"),
#     path("~update/", view=views.lara_user_update_view, name="update"),
#     path("<str:username>/", view=views.lara_user_detail_view, name="detail"),
   
    path('entities/list/', views.EntitySingleTableView.as_view(), name='entity-list'),

    path('entities/create/', views.EntityCreateView.as_view(),
         name='entity-create'),
    path('entities/update/<uuid:pk>',
         views.EntityUpdateView.as_view(), name='entity-update'),
    path('entities/delete/<uuid:pk>',
         views.EntityDeleteView.as_view(), name='entity-delete'),
    # path delete selected entities
    path('entities/delete/', views.EntityDeleteSelectedView.as_view(),
           name='entity-delete-selected'),
    path('users/list/', views.LaraUserSingleTableView.as_view(),
         name='lara-user-list'),
    path('users/create/', views.LaraUserCreateView.as_view(),
         name='lara-user-create'),
    path('users/update/<uuid:pk>', views.LaraUserUpdateView.as_view(),
         name='lara-user-update'),
    path('users/delete/<uuid:pk>', views.LaraUserDeleteView.as_view(),
         name='lara-user-delete'),

    path('entities/<uuid:pk>/', views.EntityDetailView.as_view(),
         name='entity-details'),
    path('users/<uuid:pk>/', views.LaraUserDetailView.as_view(),
         name='lara-user-details'),
    path('<uuid:pk>/', views.EntityDetailView.as_view(), name='entity-details'),
    #~ path('groups/', views.userGroups, name='user-groups'),
    path('search/', views.search_all, name='search-post'),
    path('', views.EntitySingleTableView.as_view(), name='entity-list-root'),

    #path('search-results/', views.search, name='search'),
    #path('results/', views.results, name='results'),
] 


# urlpatterns = [
#     path('', views.EntitySingleTableView.as_view(), name='entity-list-root'),
#     path('entities/list/', views.EntitySingleTableView.as_view(), name='entity-list'),
#     path('addresses/list/', views.AddressesListView.as_view(), name='address-list'),
#     path('addresses/create/', views.AddressCreateView.as_view(),
#          name='address-create'),
#     path('addresses/update/<uuid:pk>', views.AddressUpdateView.as_view(),
#          name='address-update'),
#     path('addresses/delete/<uuid:pk>', views.AddressDeleteView.as_view(),
#          name='address-delete'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# register handlers in settings
grpc_settings.user_settings["GRPC_HANDLERS"] += [
   "lara_django_people.grpc.handlers.grpc_handlers"]
