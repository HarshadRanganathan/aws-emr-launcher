from json import load
from yaml import safe_load
from emrlauncher.utils import dict_merge, substitute_placeholders_with_values


class ConfigParser(object):
    """
    ConfigParser: Parses the configuration files and substitutes placeholders with input variables
    """
    EMR = 'Emr'

    def __init__(self):
        self.default_config = dict()
        self.env_config = dict()
        self.app_config = dict()
        self.flow_config = dict()
        self.cluster_config = dict()

    def _get_app_configuration(self, default_config_path, env_config_path, input_vars):
        """ Returns merged application configuration data
        :param default_config_path: Default configuration file path
        :param env_config_path: Environment specific configuration file path
        :param input_vars: Input variables which serve as parameters for the configuration files
        :return:
        """
        with open(default_config_path, 'r') as dc:
            default_config_data = dc.read()
            self.default_config = safe_load(substitute_placeholders_with_values(default_config_data, input_vars))
        with open(env_config_path, 'r') as ec:
            env_config_data = ec.read()
            self.env_config = safe_load(substitute_placeholders_with_values(env_config_data, input_vars))
        return dict_merge(self.default_config, self.env_config)

    @staticmethod
    def _get_cluster_configuration(cluster_config_path):
        with open(cluster_config_path) as cc:
            return load(cc)

    def load_configuration(self, cluster_config_path, default_config_path, env_config_path, input_vars):
        self.app_config = self._get_app_configuration(default_config_path, env_config_path, input_vars)
        self.flow_config = self.app_config.get(self.EMR, [])
        self.cluster_config = self._get_cluster_configuration(cluster_config_path)
