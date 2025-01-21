# LARA-django People

The lara_people application can be used to organise people and institutions in the LARA database.

## Installation

In the active LARA-django environment, install

    cd  lara_django_people
    pip install .


Add "my_new_app" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [
        ...
        ' lara_django_people',
    ]

Include the lara-django-app URLconf in your project urls.py like
this:

    path(' lara_django_people', include('my_new_app.urls')),

Run 

    python manage.py makemigrations  lara_django_people
    python manage.py migrate 
    
to create the my_new_app database models.


In case you like to test the app, please load the demo data:

Start the development server 

    lara-django-dev runserver

and visit

http://127.0.0.1:8000/admin/ 

to create some entries (you'll need the Admin app enabled).


## Environment variables

for development, please set

    export DJANGO_ALLOWED_HOSTS=localhost
    export DJANGO_SETTINGS_MODULE=lara_django.settings.devel

for production, please set 

    export DJANGO_SETTINGS_MODULE=lara_django.settings.production

if your media does not reside in the default media folder, please set
environment variable to 

    export DJANGO_MEDIA_PATH='path/to/my/media'

to use user defined fixtures, please set: :: export
    
    DJANGO_FIXTURE_PATH='path/to/user/fixtures'


Testing all applications

## Basic Commands

### Type checks

Running type checks with mypy:

    $ mypy lara_django_people

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest


[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: GPLv3

