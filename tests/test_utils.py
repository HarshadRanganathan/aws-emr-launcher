import pytest
from emrlauncher.utils import dict_merge, substitute_placeholders_with_values


@pytest.fixture
def input_vars():
    return {"ENVIRONMENT": "prod", "VERSION": "1.0", "REGION": "us-east-1"}


@pytest.mark.parametrize(
    "data,expected",
    [
        ("${ENVIRONMENT}-data-loading-cluster", "prod-data-loading-cluster"),
        (
            "s3://elasticmapreduce/amiroller/AWSJavaClientRuntime-${VERSION}.jar",
            "s3://elasticmapreduce/amiroller/AWSJavaClientRuntime-1.0.jar",
        ),
        (
            "bootstrap: \
        script_path: 's3://elasticmapreduce/backup/libs/hive/0.7/install-hive.sh' \
        args: [--region, '${REGION}']",
            "bootstrap: \
        script_path: 's3://elasticmapreduce/backup/libs/hive/0.7/install-hive.sh' \
        args: [--region, 'us-east-1']",
        ),
    ],
)
def test_substitute_placeholders_with_values(input_vars, data, expected):
    assert substitute_placeholders_with_values(data, input_vars) == expected


@pytest.mark.parametrize(
    "dict1,dict2,expected",
    [
        (
            {"regions": ["us-east-1"], "name": "data-loading-cluster"},
            {"regions": ["us-east-1", "us-west-2", "eu-west-1"]},
            {
                "regions": ["us-east-1", "us-west-2", "eu-west-1"],
                "name": "data-loading-cluster",
            },
        ),
        (
            {"name": "data-loading-cluster"},
            {"regions": ["us-east-1", "us-west-2", "eu-west-1"]},
            {
                "regions": ["us-east-1", "us-west-2", "eu-west-1"],
                "name": "data-loading-cluster",
            },
        ),
        (
            {"emr": {"name": "data-loading-cluster"}},
            {"emr": {"regions": ["us-east-1", "us-west-2", "eu-west-1"]}},
            {
                "emr": {
                    "name": "data-loading-cluster",
                    "regions": ["us-east-1", "us-west-2", "eu-west-1"],
                }
            },
        ),
    ],
)
def test_dict_merge(dict1, dict2, expected):
    assert dict_merge(dict1, dict2) == expected
