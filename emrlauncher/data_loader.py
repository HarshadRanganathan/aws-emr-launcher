from typing import List, Dict
import logging
import ast
import boto3

from emrlauncher.config_parser import ConfigParser
from emrlauncher.emr_launcher import EmrLauncher
from emrlauncher.utils import substitute_placeholders_with_values

SESSION = boto3.session.Session()

LOGGER = logging.getLogger(__name__)


def trigger_data_load(
        regions: List[str],
        cluster_config_path: str,
        default_config_path: str,
        env_config_path: str,
        input_vars: Dict[str, str],
) -> dict:
    """
    :param regions: AWS regions in which the EMR job needs to be triggered
    :type regions: list
    :param cluster_config_path: EMR cluster configuration file path
    :type cluster_config_path: str
    :param default_config_path: Default configuration file path
    :type default_config_path: str
    :param env_config_path: Environment specific configuration file path
    :type env_config_path: str
    :param input_vars: Input variables which serve as parameters for the configuration files
    :type input_vars: dict
    :return:
    """
    config_parser = ConfigParser()
    config_parser.load_configuration(
        cluster_config_path, default_config_path, env_config_path, input_vars
    )

    for region in regions:

        input_vars["REGION"] = region  # expose runtime information

        if region in config_parser.flow_config:
            emr_client = SESSION.client(service_name="emr", region_name=region)
            emr_launcher = EmrLauncher(emr_client)

            runtime_flow_config = ast.literal_eval(
                substitute_placeholders_with_values(
                    str(config_parser.flow_config), input_vars
                )
            )

            response = emr_launcher.create_cluster(
                flow_config=runtime_flow_config,
                cluster_config=config_parser.cluster_config,
                region=region,
            )

            for step in runtime_flow_config["Steps"]:
                emr_launcher.add_step(
                    step_name=step.get("Name"),
                    action_on_failure=step.get("ActionOnFailure"),
                    args=step.get("Args"),
                )

            return response
        else:
            raise Exception("Instance config missing for region {}".format(region))
