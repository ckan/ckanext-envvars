import logging
import os

import ckan.plugins as plugins
import ckantoolkit as toolkit

if toolkit.check_ckan_version(min_version='2.10'):
    from ckan.common import config_declaration
else:
    config_declaration = None


log = logging.getLogger(__name__)


class EnvvarsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # This is only used on CKAN>=2.10
    declared_keys = None

    def _envvar_to_ini(self, key):
        '''Transforms an env var formatted key to ini formatting.'''

        def _format_key(key):
            # Set it to lowercase
            key = key.lower()
            # Replace dunders with dots
            key = key.replace('__', '.')

            return key

        # If the key starts with 'CKAN___' (3 underscores).
        if key.startswith('CKAN___'):
            key = key[7:]

        if self.declared_keys:
            # If the key is defined as present in the env var, leave as is
            # (eg uppercase)
            if key not in self.declared_keys:
                key = _format_key(key)
        else:
            key = _format_key(key)

        return key

    # IConfigurer

    def update_config(self, config):

        # get all vars beginning with 'CKAN'
        ckan_vars = ((k, v) for k, v in os.environ.items()
                     if k.startswith('CKAN'))

        if config_declaration:
            self.declared_keys = [str(k) for k in config_declaration.iter_options()]
            # SECRET_KEY is marked as internal in CKAN 2.10 but we want to
            # encourage its use so we support it here
            if "SECRET_KEY" not in self.declared_keys:
                self.declared_keys.append("SECRET_KEY")
        else:
            self.declared_keys = None

        # transform vars into ini settings format
        ckan_vars = ((self._envvar_to_ini(k), v) for k, v in ckan_vars)

        # override config settings with new values
        config.update(dict(ckan_vars))

        # CKAN >=2.10 normalizes config values
        if config_declaration:
            config_declaration.normalize(config)
