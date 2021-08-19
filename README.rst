.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://github.com/GSA/ckanext-envvars/actions/workflows/test.yml/badge.svg
    :target: https://github.com/GSA/ckanext-envvars/actions


===============
ckanext-envvars
===============

This CKAN extension checks for environmental variables conforming to an
expected format and updates the corresponding CKAN config settings with its
value.

For the extension to correctly identify which env var keys map to the format
used for the config object, env var keys should be formatted in the following
way:

1) All uppercase
2) Replace periods ('.') with two underscores ('__')
3) Keys must begin with 'CKAN' or 'CKANEXT'

Some examples::

    ckan.site_id --> CKAN__SITE_ID
    ckanext.s3filestore.aws_bucket_name --> CKANEXT__S3FILESTORE__AWS_BUCKET_NAME

For keys that don't normally begin with 'CKAN', add 'CKAN___' (3 underscores)
to the beginning to help the extension identify these keys, e.g.::

    sqlalchemy.url --> CKAN___SQLALCHEMY__URL
    beaker.session.secret --> CKAN___BEAKER__SESSION__SECRET


------------
Requirements
------------

Parent Repo --> Tested in CKAN 2.3 and 2.4.0, but may work in previous versions.
This fork   --> Tested in CKAN 2.8 and CKAN 2.9, but may work in other versions.

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

Using the Docker Dev Environment
================================

Build Environment
-----------------

To start environment, run:
```make build```
```make up```

CKAN will start at localhost:5000

To shut down environment, run:

  ```make clean```

To docker exec into the CKAN image, run:

  ```docker-compose exec app /bin/bash```

Testing
-------

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the extension tests, start the containers with `make up`, then:

    $ make test

Lint the code.

    $ make lint
    
Matrix builds
-------------

The existing development environment assumes a full catalog.data.gov test setup. This makes
it difficult to develop and test against new versions of CKAN (or really any
dependency) because everything is tightly coupled and would require us to
upgrade everything at once which doesn't really work. A new make target
`test-new` is introduced with a new docker-compose file.

The "new" development environment drops as many dependencies as possible. It is
not meant to have feature parity with
[GSA/catalog.data.gov](https://github.com/GSA/catalog.data.gov/). Tests should
mock external dependencies where possible.

In order to support multiple versions of CKAN, or even upgrade to new versions
of CKAN, we support development and testing through the `CKAN_VERSION`
environment variable.

    $ make CKAN_VERSION=2.8 test
    $ make CKAN_VERSION=2.9 test


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
