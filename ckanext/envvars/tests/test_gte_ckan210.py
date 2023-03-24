import os
import pytest
import ckan.plugins as p
from ckantoolkit import config
import ckantoolkit as toolkit


if toolkit.check_ckan_version(max_version='2.9.99'):
    pytest.skip("Skipping CKAN < 2.10", allow_module_level=True)


from unittest import mock


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

    @mock.patch('ckanext.datastore.plugin.DatastorePlugin.configure')
    def test_core_ckan_envvar_values_in_config(self, datastore_configure):

        if not toolkit.check_ckan_version('2.4.0'):
            raise pytest.skip('CKAN version 2.4 or above needed')

        core_ckan_env_var_list = [
            ('CKAN_SQLALCHEMY_URL', 'postgresql://mynewsqlurl/'),
            ('CKAN_DATASTORE_WRITE_URL', 'postgresql://mynewdbwriteurl/'),
            ('CKAN_DATASTORE_READ_URL', 'postgresql://mynewdbreadurl/'),
            ('CKAN_SITE_ID', 'my-site'),
            ('CKAN_DB', 'postgresql://mydeprectatesqlurl/'),
            ('CKAN_SMTP_SERVER', 'mail.example.com'),
            ('CKAN_SMTP_STARTTLS', 'True'),
            ('CKAN_SMTP_USER', 'my_user'),
            ('CKAN_SMTP_PASSWORD', 'password'),
            ('CKAN_SMTP_MAIL_FROM', 'server@example.com'),
            ('CKAN__DATASETS_PER_PAGE', '14'),
            ('CKAN__HIDE_ACTIVITY_FROM_USERS', 'user1 user2'),
        ]

        self._setup_env_vars(core_ckan_env_var_list)

        assert config['sqlalchemy.url'] == 'postgresql://mynewsqlurl/'
        assert config['ckan.datastore.write_url'] == 'postgresql://mynewdbwriteurl/'
        assert config['ckan.datastore.read_url'] == 'postgresql://mynewdbreadurl/'
        assert config['ckan.site_id'] == 'my-site'
        assert config['smtp.server'] == 'mail.example.com'
        assert config['smtp.starttls'] == 'True'
        assert config['smtp.user'] == 'my_user'
        assert config['smtp.password'] == 'password'
        assert config['smtp.mail_from'] == 'server@example.com'
        # I'll expect CKAN 2.10 to transform this to an int
        assert config['ckan.datasets_per_page'] == 14
        assert config['ckan.hide_activity_from_users'] == ['user1',  'user2']

        self._teardown_env_vars(core_ckan_env_var_list)

    @mock.patch('ckanext.datastore.plugin.DatastorePlugin.configure')
    def test_core_ckan_envvar_values_in_config_take_precedence(self, datastore_configure):
        '''Core CKAN env var transformations take precedence over this
        extension'''

        combined_list = [
            ('CKAN___SQLALCHEMY__URL', 'postgresql://thisextensionformat/'),
            ('CKAN_SQLALCHEMY_URL', 'postgresql://coreckanformat/'),
        ]

        self._setup_env_vars(combined_list)

        assert config['sqlalchemy.url'] == 'postgresql://coreckanformat/'

        self._teardown_env_vars(combined_list)
