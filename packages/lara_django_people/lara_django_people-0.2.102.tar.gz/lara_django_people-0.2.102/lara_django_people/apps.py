"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people app *

:details: lara_django_people app configuration. 
         This provides a generic django app configuration mechanism.
         For more details see:
         https://docs.djangoproject.com/en/4.0/ref/applications/
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""


from django.apps import AppConfig


class LaraDjangoPeopleConfig(AppConfig):
    name = 'lara_django_people'
    url_path = 'people/'
    # enter a verbose name for your app: lara_django_people here - this will be used in the admin interface
    verbose_name = 'LARA-django People'
    lara_app_icon = 'lara_people_icon.svg'  # this will be used to display an icon, e.g. in the main LARA menu.
    lara_app_color = 'blue'  # this color will be used to display the app in the main LARA menu.
    verbose_name_short = "People"
    lara_app_description = "People and Organizations"
    lara_class_apps = [
        {
            "name": "People",
            "path":  "lara_django_people:entity-list", # "/projects/project/list",
            "icon": "lara_projects_icon.svg",
            "color": lara_app_color,
        },
        {
            "name": "Institutions & Companies",
            "path":  "lara_django_people:entity-list", # "/projects/project/list",
            "icon": "lara_projects_icon.svg",
            "color": lara_app_color,
        },
        
    ]
    lara_instance_apps = []

    def ready(self):
        # add urlpatterns 
        from django.urls import path, include
        from lara_django.urls import urlpatterns

        urlpatterns += [ 
            path(self.url_path, include('lara_django_people.urls', namespace='lara_django_people')),
        ]

        # import lara_django_people.grpc
