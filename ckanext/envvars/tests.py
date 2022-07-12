import os
import pytest

import ckan.plugins as p

from ckantoolkit import config
import ckantoolkit as toolkit

from ckanext.envvars.plugin import EnvvarsPlugin


class TestEnvVarToIni(object):

    def test_envvartoini_expected_output(self):
        '''
        EnvvarsPlugin._envvar_to_ini returns expected transformation of env
        var formated keys
        '''

        envvar_to_ini_examples = [
            ('CKAN___CKAN__SITE_ID', 'ckan.site_id'),
            ('CKAN__SITE_ID', 'ckan.site_id'),
            ('CKAN___CKANEXT__EXTENSION_SETTING', 'ckanext.extension_setting'),
            ('CKANEXT__EXTENSION_SETTING', 'ckanext.extension_setting'),
            ('CKAN___BEAKER__SESSION__KEY', 'beaker.session.key'),
            ('CKAN___CACHE_DIR', 'cache_dir'),
            ('CKAN___CKAN__FEEDS__AUTHORITY_NAME',
                'ckan.feeds.authority_name'),
            ('CKAN__FEEDS__AUTHORITY_NAME', 'ckan.feeds.authority_name'),
        ]

        for envkey, inikey in envvar_to_ini_examples:
            assert EnvvarsPlugin._envvar_to_ini(envkey) == inikey


class TestEnvVarsConfig(object):

    def _setup_env_vars(self, envvar_list):
        for env_var, value in envvar_list:
            os.environ[env_var] = value
        # plugin.load() will force the config to update
        p.load()

    def _teardown_env_vars(self, envvar_list):
        for env_var, _ in envvar_list:
            if os.environ.get(env_var, None):
                del os.environ[env_var]
        # plugin.load() will force the config to update
        p.load()

    def test_envvars_values_in_config(self):
        envvar_to_ini_examples = [
            ('CKAN__SITE_ID', 'my-envvar-site'),
            ('CKAN___CKANEXT__EXTENSION_SETTING', 'my-extension-value'),
            ('CKANEXT__ANOTHER__EXT_SETTING', 'my-other-extension-value'),
            ('CKAN___BEAKER__SESSION__KEY', 'my-beaker-key'),
            ('CKAN___CACHE_DIR', '/cache_directory_path/'),
        ]

        self._setup_env_vars(envvar_to_ini_examples)

        assert config['ckan.site_id'] == 'my-envvar-site'
        assert config['ckanext.extension_setting'] == 'my-extension-value'
        assert config['ckanext.another.ext_setting'] == 'my-other-extension-value'
        assert config['beaker.session.key'] == 'my-beaker-key'
        assert config['cache_dir'] == '/cache_directory_path/'

        self._teardown_env_vars(envvar_to_ini_examples)


class TestCkanCoreEnvVarsConfig(object):

    '''
    Some values are are transformed into ini settings by core CKAN. These
    tests makes sure they still work.
    '''

    def _setup_env_vars(self, envvar_list):
        for env_var, value in envvar_list:
            os.environ[env_var] = value
        # plugin.load() will force the config to update
        p.load()

    def _teardown_env_vars(self, envvar_list):
        for env_var, _ in envvar_list:
            if os.environ.get(env_var, None):
                del os.environ[env_var]
        # plugin.load() will force the config to update
        p.load()

    def test_core_ckan_envvar_values_in_config(self):

        if not toolkit.check_ckan_version('2.4.0'):
            raise pytest.skip('CKAN version 2.4 or above needed')

        core_ckan_env_var_list = [
            ('CKAN_SQLALCHEMY_URL', 'postgresql://mynewsqlurl/'),
            ('CKAN_DATASTORE_WRITE_URL', 'http://mynewdbwriteurl/'),
            ('CKAN_DATASTORE_READ_URL', 'http://mynewdbreadurl/'),
            ('CKAN_SITE_ID', 'my-site'),
            ('CKAN_DB', 'postgresql://mydeprectatesqlurl/'),
            ('CKAN_SMTP_SERVER', 'mail.example.com'),
            ('CKAN_SMTP_STARTTLS', 'True'),
            ('CKAN_SMTP_USER', 'my_user'),
            ('CKAN_SMTP_PASSWORD', 'password'),
            ('CKAN_SMTP_MAIL_FROM', 'server@example.com')
        ]

        self._setup_env_vars(core_ckan_env_var_list)

        assert config['sqlalchemy.url'] == 'postgresql://mynewsqlurl/'
        assert config['ckan.datastore.write_url'] == 'http://mynewdbwriteurl/'
        assert config['ckan.datastore.read_url'] == 'http://mynewdbreadurl/'
        assert config['ckan.site_id'] == 'my-site'
        assert config['smtp.server'] == 'mail.example.com'
        assert config['smtp.starttls'] == 'True'
        assert config['smtp.user'] == 'my_user'
        assert config['smtp.password'] == 'password'
        assert config['smtp.mail_from'] == 'server@example.com'

        self._teardown_env_vars(core_ckan_env_var_list)

    def test_core_ckan_envvar_values_in_config_take_precedence(self):
        '''Core CKAN env var transformations take precedence over this
        extension'''

        if not toolkit.check_ckan_version('2.4.0'):
            raise pytest.skip('CKAN version 2.4 or above needed')

        combined_list = [
            ('CKAN___SQLALCHEMY__URL', 'postgresql://thisextensionformat/'),
            ('CKAN_SQLALCHEMY_URL', 'postgresql://coreckanformat/'),
        ]

        self._setup_env_vars(combined_list)

        assert config['sqlalchemy.url'] == 'postgresql://coreckanformat/'

        self._teardown_env_vars(combined_list)
