# django-polls

A simple and reusable polls application for django.

## Key features

* basic poll handling (poll, choices, votes)
* easy to extend

## Installation

<!-- If you want to install the latest stable release from PyPi:

    $ pip install django-polls -->

<!-- If you want to install the latest development version from GitHub: -->
Ensure that Git is installed and available in your command-line environment by running:
    $ git --version

Install the latest version from GitHub:

    $ pip install -e git://github.com/ahteshamtariq/django-polls#egg=django-polls

If there is `Operation timed out` while installing with above command please use:

    $ pip install -e git+https://github.com/ahteshamtariq/django-polls#egg=django-polls

Add `polls` to your `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'polls',
        ...
    )

Hook this app into your ``urls.py``:

    urlpatterns = patterns('',
        ...
        url(r'^polls/', include('polls.urls', namespace='polls')),
        ...
    )
