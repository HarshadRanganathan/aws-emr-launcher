import logging
import datetime

LOGGER = logging.getLogger(__name__)


class EmrLauncher:
    """
    Emr: object to launch EMR cluster and add steps to the job flow
    """

    NAME = "Name"
    LOG_URI = "LogUri"
    RELEASE_LABEL = "ReleaseLabel"
    INSTANCES = "Instances"
    BOOTSTRAP_ACTIONS = "BootstrapActions"
    APPLICATIONS = "Applications"
    VISIBLE_TO_ALL_USERS = "VisibleToAllUsers"
    JOB_FLOW_ROLE = "JobFlowRole"
    SERVICE_ROLE = "ServiceRole"
    TAGS = "Tags"
    EMR_JOB_FLOW_DEFAULT = "EMRJobflowDefault"

    def __init__(self, client):
        self.client = client
        self.cluster_id = None

    @staticmethod
    def _get_startup_timestamp():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")

    def create_cluster(
            self, flow_config: dict, cluster_config: list, region: str
    ) -> dict:
        """ creates and starts running a new cluster
        create_cluster:
        :param flow_config: emr job flow settings
        :type flow_config: dict
        :param cluster_config: configurations for an EMR cluster instance group
        :type cluster_config: list
        :param region: aws region
        :type region: str
        :return: result of job flow operation
        """
        log_uri = flow_config.get(self.LOG_URI) + self._get_startup_timestamp()

        response = self.client.run_job_flow(
            Name=flow_config.get(self.NAME),
            LogUri=log_uri,
            ReleaseLabel=flow_config.get(self.RELEASE_LABEL, None),
            Instances=flow_config.get(region).get(self.INSTANCES),
            Applications=flow_config.get(self.APPLICATIONS, []),
            BootstrapActions=flow_config.get(self.BOOTSTRAP_ACTIONS, []),
            Configurations=cluster_config,
            VisibleToAllUsers=True,
            JobFlowRole=flow_config.get(region).get(
                self.JOB_FLOW_ROLE, self.EMR_JOB_FLOW_DEFAULT
            ),
            ServiceRole=flow_config.get(region).get(self.SERVICE_ROLE),
            Tags=flow_config.get(self.TAGS, {}),
        )

        self.cluster_id = response.get("JobFlowId")
        logging.info("New Cluster [%s] running in region [%s]", self.cluster_id, region)

        return response

    @staticmethod
    def _step_definition(step_name: str, action_on_failure: str, args: list) -> dict:
        """
        _step_definition: job flow step
        :param step_name: name of the step
        :type step_name: str
        :param action_on_failure: action to take if the step fails
        :type action_on_failure: str
        :param args: list of command line arguments passed to the JAR file's main function when executed
        :type args: list
        :return: step config
        """
        return {
            "Name": step_name,
            "ActionOnFailure": action_on_failure,
            "HadoopJarStep": {"Jar": "command-runner.jar", "Args": args},
        }

    def add_step(self, step_name: str, action_on_failure: str, args: list) -> dict:
        """
        add_step: add new step to job flow
        :param step_name: name of the step
        :type step_name: str
        :param action_on_failure: action to take if the step fails
        :type action_on_failure: str
        :param args: list of command line arguments passed to the JAR file's main function when executed
        :type args: list
        :return: step config
        """
        if self.cluster_id is None:
            raise ValueError("Cluster needs to be provisioned first!!")

        step = self._step_definition(
            step_name=step_name, action_on_failure=action_on_failure, args=args
        )

        response = self.client.add_job_flow_steps(
            JobFlowId=self.cluster_id, Steps=[step]
        )

        logging.info("Step [%s] added to cluster [%s]", step_name, self.cluster_id)

        return response
