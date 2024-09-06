import os

import pytest

import ckan.plugins as p
import ckantoolkit as tk
from ckanext.envvars.plugin import EnvvarsPlugin


if tk.check_ckan_version(min_version='2.10'):
    from unittest import mock
else:
    import mock


class MockPluginEnvVars(p.SingletonPlugin):
    pass


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
            assert EnvvarsPlugin()._envvar_to_ini(envkey) == inikey

    @pytest.mark.skipif(tk.check_ckan_version(max_version='2.10'), reason="This does not apply to CKAN<2.10")
    def test_envvartoini_expected_output_declared_option(self):
        '''
        EnvvarsPlugin._envvar_to_ini returns expected transformation of env
        var formated keys
        '''

        envvar_to_ini_examples = [
            ('CKAN___SECRET_KEY', 'SECRET_KEY'),
            ('CKAN___REMEMBER_COOKIE_DURATION', 'REMEMBER_COOKIE_DURATION'),
            ('CKAN___WTF_CSRF_ENABLED', 'WTF_CSRF_ENABLED'),
            ('CKAN___NOT_DECLARED', 'not_declared'),
        ]

        for envkey, inikey in envvar_to_ini_examples:
            assert EnvvarsPlugin()._envvar_to_ini(envkey) == inikey


class EnvVarsTestBase(object):

    def _setup_env_vars(self, envvar_list):
        for env_var, value in envvar_list:
            os.environ[env_var] = value

        # Force a config update
        p.plugins_update()

    def _teardown_env_vars(self, envvar_list):
        for env_var, _ in envvar_list:
            if os.environ.get(env_var, None):
                del os.environ[env_var]

        # Force a config update
        p.plugins_update()


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.ckan_config("ckan.plugins", "envvars")
class TestEnvVarsConfig(EnvVarsTestBase):

    def test_envvars_values_in_config(self):
        envvar_to_ini_examples = [
            ('CKAN__SITE_ID', 'my-envvar-site'),
            ('CKAN___CKANEXT__EXTENSION_SETTING', 'my-extension-value'),
            ('CKANEXT__ANOTHER__EXT_SETTING', 'my-other-extension-value'),
            ('CKAN___BEAKER__SESSION__KEY', 'my-beaker-key'),
            ('CKAN___CACHE_DIR', '/cache_directory_path/'),
        ]

        self._setup_env_vars(envvar_to_ini_examples)

        assert tk.config['ckan.site_id'] == 'my-envvar-site'
        assert tk.config['ckanext.extension_setting'] == 'my-extension-value'
        assert tk.config['ckanext.another.ext_setting'] == 'my-other-extension-value'
        assert tk.config['beaker.session.key'] == 'my-beaker-key'
        assert tk.config['cache_dir'] == '/cache_directory_path/'

        self._teardown_env_vars(envvar_to_ini_examples)

    @pytest.mark.skipif(tk.check_ckan_version(max_version='2.10'), reason="This does not apply to CKAN<2.10")
    def test_envvars_values_in_config(self):

        envvar_to_ini_examples = [
            ('CKAN___SECRET_KEY', 'super_secret'),
            ('CKAN___REMEMBER_COOKIE_DURATION', '1000'),
            ('CKAN___WTF_CSRF_ENABLED', 'True'),
            ('CKAN___NOT_DECLARED', 'test'),
        ]

        self._setup_env_vars(envvar_to_ini_examples)

        assert tk.config['SECRET_KEY'] == 'super_secret'
        assert tk.config['REMEMBER_COOKIE_DURATION'] == 1000
        assert tk.config['WTF_CSRF_ENABLED'] == True
        assert tk.config['not_declared'] == 'test'

        self._teardown_env_vars(envvar_to_ini_examples)


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.ckan_config("ckan.plugins", "envvars")
class TestCkanCoreEnvVarsConfig(EnvVarsTestBase):

    '''
    Some values are are transformed into ini settings by core CKAN. These
    tests makes sure they still work.
    '''

    # The datastore plugin, only for CKAN 2.10+, will try to
    # connect to the database when it is loaded.
    @mock.patch('ckanext.datastore.plugin.DatastorePlugin.configure')
    def test_core_ckan_envvar_values_in_config(self, datastore_configure):

        core_ckan_env_var_list = [
            ('CKAN_SQLALCHEMY_URL', 'postgresql://mynewsqlurl/'),
            ('CKAN_DATASTORE_WRITE_URL', 'postgresql://mynewdbwriteurl/'),
            ('CKAN_DATASTORE_READ_URL', 'postgresql://mynewdbreadurl/'),
            ('CKAN_SITE_ID', 'my-site'),
            ('CKAN_DB', 'postgresql://mydeprectatesqlurl/'),
            # SMTP settings takes precedence from CKAN core CONFIG_FROM_ENV_VARS
            ('CKAN_SMTP_SERVER', 'mail.example.com'),
            ('CKAN_SMTP_STARTTLS', 'True'),
            ('CKAN_SMTP_USER', 'my_user'),
            ('CKAN_SMTP_PASSWORD', 'password'),

            ('CKAN_SMTP_MAIL_FROM', 'server@example.com'),
            ('CKAN__DATASETS_PER_PAGE', '14'),
            ('CKAN__HIDE_ACTIVITY_FROM_USERS', 'user1 user2'),
        ]

        self._setup_env_vars(core_ckan_env_var_list)

        assert tk.config['sqlalchemy.url'] == 'postgresql://mynewsqlurl/'
        assert tk.config['ckan.datastore.write_url'] == 'postgresql://mynewdbwriteurl/'
        assert tk.config['ckan.datastore.read_url'] == 'postgresql://mynewdbreadurl/'
        assert tk.config['ckan.site_id'] == 'my-site'
        assert tk.config['smtp.server'] == 'mail.example.com'

        assert tk.config['smtp.user'] == 'my_user'
        assert tk.config['smtp.password'] == 'password'
        assert tk.config['smtp.mail_from'] == 'server@example.com'
        if tk.check_ckan_version(min_version='2.10'):
            assert tk.config['smtp.starttls'] is True
        else:
            assert tk.config['smtp.starttls'] == 'True'


        if tk.check_ckan_version(min_version='2.10'):
            assert tk.config['ckan.datasets_per_page'] == 14
            assert tk.config['ckan.hide_activity_from_users'] == ['user1', 'user2']
        else:
            assert tk.config['ckan.datasets_per_page'] == '14'
            assert tk.config['ckan.hide_activity_from_users'] == 'user1 user2'

        self._teardown_env_vars(core_ckan_env_var_list)

    @pytest.mark.skipif(tk.check_ckan_version(min_version='2.11'), reason="This does not apply to CKAN>=2.11")
    @mock.patch('ckanext.datastore.plugin.DatastorePlugin.configure')
    def test_core_ckan_envvar_values_in_config_take_precedence(self, datastore_configure):
        '''Core CKAN env var transformations take precedence over this
        extension in CKAN<2.11

        See https://github.com/ckan/ckan/pull/7502#issuecomment-1499049307
        '''

        combined_list = [
            ('CKAN___SQLALCHEMY__URL', 'postgresql://thisextensionformat/'),
            ('CKAN_SQLALCHEMY_URL', 'postgresql://coreckanformat/'),
        ]

        self._setup_env_vars(combined_list)

        assert tk.config['sqlalchemy.url'] == 'postgresql://coreckanformat/'

        self._teardown_env_vars(combined_list)

    @pytest.mark.skipif(tk.check_ckan_version(max_version='2.11'), reason="This does not apply to CKAN<2.11")
    @mock.patch('ckanext.datastore.plugin.DatastorePlugin.configure')
    def test_core_ckan_envvar_values_in_config_does_not_take_precedence(self, datastore_configure):
        '''This extension takes precedence over Core CKAN env var transformations in CKAN>=2.11

        See https://github.com/ckan/ckan/pull/7502#issuecomment-1499049307
        '''

        combined_list = [
            ('CKAN___SQLALCHEMY__URL', 'postgresql://thisextensionformat/'),
            ('CKAN_SQLALCHEMY_URL', 'postgresql://coreckanformat/'),
        ]

        self._setup_env_vars(combined_list)

        assert tk.config['sqlalchemy.url'] == 'postgresql://thisextensionformat/'

        self._teardown_env_vars(combined_list)

    @pytest.mark.skipif(tk.check_ckan_version(max_version='2.11'), reason="This does not apply to CKAN<2.11")
    def test_plugins_loaded(self):
        '''
        New plugins defined in CKAN__PLUGINS are loaded by ckanext-envvars
        '''

        assert not p.plugin_loaded("mock_envvars_plugin")

        combined_list = [
            ('CKAN__PLUGINS', 'mock_envvars_plugin envvars'),
        ]

        self._setup_env_vars(combined_list)

        assert p.plugin_loaded("mock_envvars_plugin")

        self._teardown_env_vars(combined_list)
