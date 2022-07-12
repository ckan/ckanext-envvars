[![image](https://github.com/okfn/ckanext-envvars/actions/workflows/test.yml/badge.svg)](https://github.com/okfn/ckanext-envvars/actions)

ckanext-envvars
===============

This CKAN extension checks for environmental variables conforming to an
expected format and updates the corresponding CKAN config settings with
its value.

For the extension to correctly identify which env var keys map to the
format used for the config object, env var keys should be formatted in
the following way:

1)  All uppercase
2)  Replace periods (\'.\') with two underscores (\'\_\_\')
3)  Keys must begin with \'CKAN\' or \'CKANEXT\'

Some examples:

    ckan.site_id --> CKAN__SITE_ID
    ckanext.s3filestore.aws_bucket_name --> CKANEXT__S3FILESTORE__AWS_BUCKET_NAME

For keys that don\'t normally begin with \'CKAN\', add \'CKAN\_\_\_\' (3
underscores) to the beginning to help the extension identify these keys,
e.g.:

    sqlalchemy.url --> CKAN___SQLALCHEMY__URL
    beaker.session.secret --> CKAN___BEAKER__SESSION__SECRET

Requirements
------------

Tested in CKAN 2.7, CKAN 2.8 and CKAN 2.9, but may work in other
versions.

To ensure all config settings are overridden by env var values,
`envvars` must be the last plugin entry in the `ckan.plugins` list (see
\'Installation\' below).

Installation
------------

To install ckanext-envvars:

1.  Activate your CKAN virtual environment, for example:

        . /usr/lib/ckan/default/bin/activate

2.  Install the ckanext-envvars Python package into your virtual
    environment:

        pip install ckanext-envvars

3.  Add `envvars` to the `ckan.plugins` setting in your CKAN config file
    (by default the config file is located at
    `/etc/ckan/default/production.ini`).

4.  Restart CKAN. For example if you\'ve deployed CKAN with Apache on
    Ubuntu:

        sudo service apache2 reload

Development Installation
------------------------

To install ckanext-envvars for development, activate your CKAN
virtualenv and do:

    git clone https://github.com/okfn/ckanext-envvars.git
    cd ckanext-envvars
    python setup.py develop
    pip install -r dev-requirements.txt

Running the Tests
-----------------

They follow the guidelines for [testing CKAN extensions](https://docs.ckan.org/en/2.8/extensions/testing-extensions.html#testing-extensions).

To run the tests, do:

> pytest --ckan-ini=test.ini ckanext/envvars/tests.py

Registering ckanext-envvars on PyPI
-----------------------------------

ckanext-envvars should be availabe on PyPI as
<https://pypi.python.org/pypi/ckanext-envvars>. If that link doesn\'t
work, then you can register the project on PyPI for the first time by
following these steps:

1.  Create a source distribution of the project:

        python setup.py sdist

2.  Register the project:

        python setup.py register

3.  Upload the source distribution to PyPI:

        python setup.py sdist upload

4.  Tag the first release of the project on GitHub with the version
    number from the `setup.py` file. For example if the version number
    in `setup.py` is 0.0.1 then do:

        git tag 0.0.1
        git push --tags

Releasing a New Version of ckanext-envvars
------------------------------------------

ckanext-envvars is availabe on PyPI as
<https://pypi.python.org/pypi/ckanext-envvars>. To publish a new version
to PyPI follow these steps:

1.  Update the version number in the `setup.py` file. See [PEP
    440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers)
    for how to choose version numbers.

2.  Create a source distribution of the new version:

        python setup.py sdist

3.  Upload the source distribution to PyPI:

        python setup.py sdist upload

4.  Tag the new release of the project on GitHub with the version number
    from the `setup.py` file. For example if the version number in
    `setup.py` is 0.0.2 then do:

        git tag 0.0.2
        git push --tags
