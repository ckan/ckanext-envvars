.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/okfn/ckanext-envvars.svg?branch=master
    :target: https://travis-ci.org/okfn/ckanext-envvars

.. image:: https://coveralls.io/repos/okfn/ckanext-envvars/badge.svg
  :target: https://coveralls.io/r/okfn/ckanext-envvars


===============
ckanext-envvars
===============

This CKAN extension checks for environmental variables that conform to a
specific format and sets the corresponding CKAN config settings to its value.


------------
Requirements
------------

To ensure all config settings are overridden by env var values, ``envvars``
must be the last plugin entry in the ``ckan.plugins`` list (see 'Installation'
below).


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-envvars:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-envvars Python package into your virtual environment::

     pip install ckanext-envvars

3. Add ``envvars`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Document any optional config settings here. For example::

    # The minimum number of hours to wait before re-checking a resource
    # (optional, default: 24).
    ckanext.envvars.some_setting = some_default_value


------------------------
Development Installation
------------------------

To install ckanext-envvars for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/okfn/ckanext-envvars.git
    cd ckanext-envvars
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.envvars --cover-inclusive --cover-erase --cover-tests


-----------------------------------
Registering ckanext-envvars on PyPI
-----------------------------------

ckanext-envvars should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-envvars. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


------------------------------------------
Releasing a New Version of ckanext-envvars
------------------------------------------

ckanext-envvars is availabe on PyPI as https://pypi.python.org/pypi/ckanext-envvars.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
