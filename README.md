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
4)  Keys that do not begin with \'CKAN\', add \'CKAN\_\_\_\' (3 underscores) at the beginning.

Some examples:

    ckan.site_id --> CKAN__SITE_ID
    ckanext.s3filestore.aws_bucket_name --> CKANEXT__S3FILESTORE__AWS_BUCKET_NAME
    beaker.session.secret --> CKAN___BEAKER__SESSION__SECRET

Starting from CKAN 2.10 (and ckanext-envvars 0.0.4), if a configuration option is defined using CKAN's
[configuration declaration](https://docs.ckan.org/en/latest/maintaining/configuration.html#config-declaration)
the key is not further processed. This allows to keep eg upper case setttings like SECRET_KEY, WTF_CSRF_ENABLED, e.g:

    SECRET_KEY --> CKAN___SECRET_KEY
    WTF_CSRF_ENABLED --> CKAN___WTF_CSRF_ENABLED


Important note
--------------

CKAN requires a proper connection to a database to initialize and load plugins,
therefore `ckanext-envvars` cannot be used to set `sqlalchemy.url`.
Also, plugins are first loaded from the `ckan.ini` file so setting `CKAN__PLUGINS` will not have the desire effect.


Requirements
------------

Tested in CKAN 2.7, CKAN 2.8, CKAN 2.9 and CKAN 2.10, but may work in other
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


#### ckanext-envvars on PyPI

ckanext-envvars is availabe on PyPI as [ckanext-envvars](https://pypi.org/project/ckanext-envvars).

##### Releasing a New Version of ckanext-envvars


To release a new version of this CKAN extension you should:

 - Update the `setup.py` file with a new version number (N.N.N)
 - Tag this repo with the new version

```
git tag vN.N.N
git push --tags
```

 - Create a source distribution of the new version:

```
python setup.py sdist
```

 - Set up twine. The `$HOME/.pypirc` file must containg the following:

```
[pypi]
username = __token__
password = <the token value, including the `pypi-` prefix>
```

 - Upload the new version to PyPI:
```
pip install twine
twine check dist/*
twine upload dist/*
```
