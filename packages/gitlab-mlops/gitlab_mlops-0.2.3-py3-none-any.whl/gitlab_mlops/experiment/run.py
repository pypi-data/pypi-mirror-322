from typing import Any, Dict, Optional

from mlflow import MlflowClient

from gitlab_mlops.mlflow.exceptions import process_exception


class Run:
    """
    Represents a candidate run within an MLflow experiment.
    """

    def __init__(
        self, experiment_id: str, run_id: str, mlflow_client: MlflowClient | None = None
    ):
        """
        Initialize a Run instance.

        Args:
            experiment_id (str): The ID of the experiment this run belongs to.
            run_id (str): The unique identifier of this run (candidate).
            mlflow_client (MlflowClient, optional): The MLflow client instance to use for operations; a new one will be created if None is provided. Defaults to None.
        """
        self._experiment_id = experiment_id
        self._id = run_id
        if mlflow_client is None:
            self._mlflow_client = MlflowClient()
        else:
            self._mlflow_client = mlflow_client

    @property
    def id(self) -> str:
        return self._id

    @property
    def experiment_id(self) -> str:
        return self._experiment_id

    def log_param(self, key: str, value: Any):
        """
        Log a parameter for the current run (candidate).

        Args:
            key (str): The name of the parameter to log.
            value (Any): The value of the parameter to log. This can be of any type that MLflow supports.
        """
        self._mlflow_client.log_param(run_id=self._id, key=key, value=value)

    def get_params(self) -> Dict[str, Any]:
        """
        Retrieve all parameters associated with this run.
        Returns:
            Dict[str, Any]: A dictionary mapping parameter keys to their values.
        """
        try:
            return self._mlflow_client.get_run(run_id=self._id).data.params
        except Exception as e:
            process_exception(e)
            raise

    def log_metric(
        self,
        key: str,
        value: float,
        timestamp: int | None = None,
        step: int | None = None,
    ):
        """
        Log a metric to the run.
        Args:
            key (str): The name of the metric.
            value (float): The numeric value of the metric.
            timestamp (int, optional): The timestamp in milliseconds. Defaults to None.
            step (int, optional): The iteration or sequence number. Defaults to None.
        """
        self._mlflow_client.log_metric(
            run_id=self._id, key=key, value=value, timestamp=timestamp, step=step
        )

    def get_metrics(self) -> Dict[str, float]:
        """
        Retrieve all metrics associated with this run.
        Returns:
            Dict[str, float]: A dictionary mapping metric keys to their values.
        """
        try:
            return self._mlflow_client.get_run(run_id=self._id).data.metrics
        except Exception as e:
            process_exception(e)
            raise

    def log_artifact(self, local_path: str, artifact_path: str | None = None):
        """
        Log an artifact (local file or directory) to the run.
        Args:
            local_path (str): Path to the local file to log.
            artifact_path (str, optional): The run-relative path to log the artifact at. Defaults to None, meaning the artifact will be logged in the root of the run's artifact directory.
        """
        self._mlflow_client.log_artifact(
            run_id=self._id, local_path=local_path, artifact_path=artifact_path
        )

    def log_text(self, text: str, artifact_file: str):
        """
        Log arbitrary text as an artifact within the run.
        Args:
            text (str): The text to be logged.
            artifact_file (str): The path and filename of the file within the MLflow server to which the text will be saved.
        """
        self._mlflow_client.log_text(
            run_id=self._id, text=text, artifact_file=artifact_file
        )


def create_run(experiment_id: str) -> Run:
    """
    Create a new (candidate) run within the specified experiment.

    Args:
        experiment_id (str): The ID of the experiment in which to create the new run.

    Returns:
        Run: A new Run instance representing the created run.
    """
    mlflow_client = MlflowClient()
    run = mlflow_client.create_run(experiment_id=experiment_id)
    return Run(
        experiment_id=experiment_id, run_id=run.info.run_id, mlflow_client=mlflow_client
    )


def get_run(run_id: str) -> Optional[Run]:
    """
    Retrieve an existing MLflow run by its ID.
    Args:
        run_id (str): The unique identifier of the run to retrieve.
    Returns:
        Optional[Run]: An Run instance if found, None if no run with the given ID exists.
    """
    mlflow_client = MlflowClient()
    try:
        run = mlflow_client.get_run(run_id=run_id)
        if not run:
            return None
        return Run(
            experiment_id=run.info.experiment_id,
            run_id=run.info.run_id,
            mlflow_client=mlflow_client,
        )
    except Exception as e:
        # Suppress not found errors
        if "RESOURCE_DOES_NOT_EXIST" in str(e):
            return None
        process_exception(e)
        raise
