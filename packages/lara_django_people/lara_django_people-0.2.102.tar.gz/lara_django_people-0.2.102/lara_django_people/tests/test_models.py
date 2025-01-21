from lara_django_people.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
