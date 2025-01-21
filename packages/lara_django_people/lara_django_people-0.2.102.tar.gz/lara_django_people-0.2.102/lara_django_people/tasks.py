"""_____________________________________________________________________

:PROJECT: LARAsuite

*lara_django_people celery tasks*

:details: lara_django_people celery tasks.
         - 
:authors: mark doerr <mark.doerr@uni-greifswald.de>

.. note:: -
.. todo:: - 
________________________________________________________________________
"""



from celery import shared_task

from .models import LaraUser


@shared_task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return LaraUser.objects.count()
