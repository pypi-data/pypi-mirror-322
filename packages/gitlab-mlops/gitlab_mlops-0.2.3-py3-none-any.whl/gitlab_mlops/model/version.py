import os
import re
from typing import Any, Dict, Optional

from mlflow import MlflowClient
from mlflow.entities.model_registry import ModelVersion as MLflowModelVersion

from gitlab_mlops.mlflow.exceptions import process_exception

_semver_regex = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"


class ModelVersion:
    """
    Represents a version of a model in the MLflow Model Registry.
    """

    def __init__(
        self,
        model_name: str,
        version: str,
        run_id: str,
        description: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        mlflow_client: MlflowClient | None = None,
    ):
        self._model_name = model_name
        self._version = version
        self._run_id = run_id
        self._description = description
        self._tags = tags
        if mlflow_client is None:
            self._mlflow_client = MlflowClient()
        else:
            self._mlflow_client = mlflow_client

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def version(self) -> str:
        return self._version

    @property
    def run_id(self) -> str:
        return self._run_id

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def tags(self) -> Optional[dict[str, Any]]:
        return self._tags

    def log_param(self, key: str, value: Any):
        """
        Log a parameter for the current model version.

        Args:
            key (str): The name of the parameter to log.
            value (Any): The value of the parameter to log. This can be of any type that MLflow supports.
        """
        self._mlflow_client.log_param(run_id=self._run_id, key=key, value=value)

    def get_params(self) -> Dict[str, Any]:
        """
        Get all the parameters logged for the model version.
        Returns:
            Dict[str, Any]: A dictionary where keys are parameter names and values are their respective values.
        """
        try:
            return self._mlflow_client.get_run(self._run_id).data.params
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
        Log a metric to the model version.
        Args:
            key (str): The name of the metric.
            value (float): The numeric value of the metric.
            timestamp (int, optional): The timestamp in milliseconds. Defaults to None.
            step (int, optional): The iteration or sequence number. Defaults to None.
        """
        self._mlflow_client.log_metric(
            run_id=self._run_id, key=key, value=value, timestamp=timestamp, step=step
        )

    def get_metrics(self) -> Dict[str, float]:
        """
        Retrieve all the metrics logged for the model version.
        Returns:
            Dict[str, float]: A dictionary where keys are metric names and values are their respective values.
        """
        try:
            return self._mlflow_client.get_run(self._run_id).data.metrics
        except Exception as e:
            process_exception(e)
            raise

    def log_artifact(self, local_path: str, artifact_path: str | None = None):
        """
        Log an artifact (local file or directory) to the model version.
        Args:
            local_path (str): Path to the local file to log.
            artifact_path (str, optional): The run-relative path to log the artifact at. Defaults to None, meaning the artifact will be logged in the root of the run's artifact directory.
        """
        self._mlflow_client.log_artifact(
            run_id=self._run_id, local_path=local_path, artifact_path=artifact_path
        )

    def log_text(self, text: str, artifact_file: str):
        """
        Log arbitrary text as an artifact within the model version.
        Args:
            text (str): The text to be logged.
            artifact_file (str): The path and filename of the file within the MLflow server to which the text will be saved.
        """
        self._mlflow_client.log_text(
            run_id=self._run_id, text=text, artifact_file=artifact_file
        )

    @classmethod
    def from_mlflow_model_version(
        cls,
        mlflow_model_version: MLflowModelVersion,
        mlflow_client: MlflowClient | None = None,
    ):
        """Create an instance of the ModelVersion class from a MLflow ModelVersion object.
        Returns:
            ModelVersion: Instance of ModelVersion.
        """
        semver_version = _semver_version_from_alias(mlflow_model_version.aliases)
        if not semver_version:
            raise ValueError("No valid version was returned for the model version.")

        return cls(
            model_name=mlflow_model_version.name,
            version=semver_version,
            run_id=mlflow_model_version.run_id,
            tags=mlflow_model_version.tags if mlflow_model_version.tags else None,
            description=(
                mlflow_model_version.description
                if mlflow_model_version.description
                else None
            ),
            mlflow_client=mlflow_client if mlflow_client else None,
        )


def create_model_version(
    model_name: str,
    tags: Optional[dict[str, Any]] = None,
    version: Optional[str] = None,
    description: Optional[str] = None,
    run_id: Optional[str] = None,
) -> ModelVersion:
    tags = tags or {}
    if version:
        if not re.match(_semver_regex, version):
            raise ValueError(
                f"The version '{version}' must a valid SemVer string. SemVer is available from https://semver.org. Example: '1.0.0'"
            )
        tags = {**tags, **{"gitlab.version": version}}
    source = f"runs:/{run_id}" if run_id else ""

    if os.getenv("GITLAB_CI") and os.getenv("CI_JOB_ID"):
        tags = {**tags, **{"gitlab.CI_JOB_ID": os.getenv("CI_JOB_ID")}}

    mlflow_client = MlflowClient()
    try:
        mlflow_model_version = mlflow_client.create_model_version(
            name=model_name,
            description=description,
            run_id=run_id,
            source=source,
            tags=tags,
        )
    except Exception as e:
        process_exception(e)
        raise

    return ModelVersion.from_mlflow_model_version(mlflow_model_version, mlflow_client)


def _semver_version_from_alias(aliases: list[str]) -> Optional[str]:
    """
    Extract the version used by GitLab from the aliases provided by MLflow.
    """
    semver_versions = []

    # Iterate through all provided aliases and keep only valid SemVer versions.
    # Normally the list of aliases is a single version.
    for alias in aliases:
        match = re.match(_semver_regex, alias)
        if match:
            semver_versions.append(match.group(0))

    # In the unexpected case that the list of aliases contains more than one
    # version, keep the highest one by comparing them semantically.
    if semver_versions:
        return sorted(semver_versions)[-1]

    return None


def get_model_version(
    model_name: str,
    version: str,
) -> Optional[ModelVersion]:
    """
    Get the model version given its name and version or stage.
    Args:
        model_name (str): The name of the model.
        version (str): The version of the model or its stage.
    Returns:
        Optional[ModelVersion]: The model version, if found, else None.
    """
    mlflow_client = MlflowClient()
    try:
        mlflow_model_version = mlflow_client.get_model_version(
            name=model_name, version=version
        )
        if not mlflow_model_version:
            return None
    except Exception as e:
        process_exception(e)
        raise

    return ModelVersion.from_mlflow_model_version(mlflow_model_version, mlflow_client)
