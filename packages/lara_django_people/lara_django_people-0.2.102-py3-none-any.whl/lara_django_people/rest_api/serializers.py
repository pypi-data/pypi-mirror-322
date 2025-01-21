from rest_framework import serializers

from lara_django_people.models import LaraUser


class LaraUserSerializer(serializers.ModelSerializer[LaraUser]):
    class Meta:
        model = LaraUser
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }
