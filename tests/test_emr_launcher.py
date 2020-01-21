import os
from json import loads
import pytest
import boto3
from moto import mock_emr
from emrlauncher.emr_launcher import EmrLauncher

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def flow_config():
    config_file = os.path.join(__location__, "resources/flow_config.json")
    with open(config_file, "r") as file:
        return loads(file.read())


@pytest.fixture
def cluster_config():
    config_file = os.path.join(__location__, "resources/configurations.json")
    with open(config_file, "r") as file:
        return loads(file.read())


@mock_emr
def test_create_cluster_in_3_regions(flow_config, cluster_config):
    regions = ["us-east-1", "us-west-2"]

    for region in regions:
        emr_client = boto3.client(service_name="emr", region_name=region)
        emr_launcher = EmrLauncher(client=emr_client)

        cluster_id = emr_launcher.create_cluster(
            flow_config=flow_config, cluster_config=cluster_config, region=region
        )["JobFlowId"]
        cluster_details = emr_client.describe_cluster(ClusterId=cluster_id)["Cluster"]

        assert cluster_details["VisibleToAllUsers"]
        assert cluster_details["LogUri"]
        assert sorted(cluster_details["Tags"], key=lambda k: k["Key"]) == sorted(
            flow_config["Tags"], key=lambda k: k["Key"]
        )
        assert cluster_details["Applications"] == flow_config["Applications"]
        assert cluster_details["ReleaseLabel"] == flow_config["ReleaseLabel"]
        assert cluster_details["ServiceRole"] == flow_config[region]["ServiceRole"]
        assert (
            cluster_details["Ec2InstanceAttributes"]["IamInstanceProfile"]
            == flow_config[region]["JobFlowRole"]
        )
        assert (
            cluster_details["Ec2InstanceAttributes"]["Ec2SubnetId"]
            == flow_config[region]["Instances"]["Ec2SubnetId"]
        )
