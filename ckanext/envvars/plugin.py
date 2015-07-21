import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import logging
log = logging.getLogger(__name__)


class EnvvarsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config):
        log.info('updated config')
