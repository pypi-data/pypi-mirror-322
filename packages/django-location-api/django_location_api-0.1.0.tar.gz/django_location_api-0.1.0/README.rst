===================
Django Location API
===================

.. image:: https://github.com/carlosfunk/django-location-api/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/carlosfunk/django-location-api/actions/workflows/ci.yml


Django package for location services.


* Free software: BSD-3-Clause
* Documentation: https://django-location-api.readthedocs.io.


django-location-api is a Django app for location services.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "location_api" and the other required packages to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "rest_framework",
        "rest_framework_gis",
        "location_api"
    ]

2. Include the location_api URL conf in your project urls.py like this::

    path("api/", include("location_api.urls")),
    path("", include("location_api.urls.search")),

3. Run ``python manage.py migrate`` to create the location models.

4. Start the development server and visit the admin site to create a location.

5. Access the ``/locations/`` URL.

Run Tests
---------

    docker compose run --rm django python ./runtests.py


Credits
-------

This package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
