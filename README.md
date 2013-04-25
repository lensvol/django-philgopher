django-philgopher
=================

Adds support for viewing Django models over Gopher protocol. Not that you should :)

Usage
=====

1. Add philgopher to INSTALLED_APPS in your settings.py::

    INSTALLED_APPS += ['philgopher',]

2. Run, gopher, run!::

$ python ./manage.py rungopherrun

After that, connect to port 70 on any network interface and browse Django models using
highly convenient Gopher interface :)

Note: only models with verbose name in Meta subclass are eligible for browsing.


