import os
import pytest
from json import load
from emrlauncher.config_parser import ConfigParser

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def cluster_config_path():
    return os.path.abspath(os.path.join(__location__, "resources/configurations.json"))


@pytest.fixture
def default_config_path():
    return os.path.abspath(os.path.join(__location__, "resources/default.yaml"))


@pytest.fixture
def env_config_path():
    return os.path.abspath(os.path.join(__location__, "resources/prod.yaml"))


@pytest.fixture
def app_config():
    with open(
            os.path.abspath(os.path.join(__location__, "resources/app_config.json")), "r"
    ) as file:
        return load(file)


@pytest.fixture
def input_vars():
    return {"ENVIRONMENT": "prod", "VERSION": "1.0", "REGION": "us-east-1"}


def test_load_configuration(
        cluster_config_path, default_config_path, env_config_path, input_vars, app_config
):
    config_parser = ConfigParser()
    config_parser.load_configuration(
        cluster_config_path, default_config_path, env_config_path, input_vars
    )
    assert config_parser.app_config == app_config
