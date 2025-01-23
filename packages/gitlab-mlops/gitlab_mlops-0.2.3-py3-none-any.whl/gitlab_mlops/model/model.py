from typing import Any, Optional

from mlflow import MlflowClient

import gitlab_mlops.model.version as model_version
from gitlab_mlops.experiment import Experiment, get_experiment
from gitlab_mlops.mlflow.exceptions import process_exception
from gitlab_mlops.model.version import ModelVersion


class Model:

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        mlflow_client: Optional[MlflowClient] = None,
    ):
        self._name = name
        self._description = description
        if mlflow_client is None:
            self._mlflow_client = MlflowClient()
        else:
            self._mlflow_client = mlflow_client

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> Optional[str]:
        return self._description

    def create_version(
        self,
        description: Optional[str] = None,
        tags: Optional[dict[str, Any]] = None,
        version: Optional[str] = None,
        run_id: Optional[str] = None,
    ) -> model_version.ModelVersion:
        """
        Create a new model version with optional description, tags, version, and run_id.

        Args:
            description (Optional[str]): An optional description for the model version.
            tags (Optional[dict[str, Any]]): An optional dictionary of tags for the model version.
            version (Optional[str]): An optional version string for the model version, following the Semantic Versioning (SemVer) specification.
            run_id (Optional[str]): An optional run_id for the model version.
        Returns:
            ModelVersion: The newly created ModelVersion object.
        """
        return model_version.create_model_version(
            model_name=self._name,
            tags=tags,
            version=version,
            description=description,
            run_id=run_id,
        )

    def get_latest_version(self) -> Optional[ModelVersion]:
        """
        Retrieve the latest model version for this model.
        Returns:
            Optional[ModelVersion]: The latest ModelVersion object if found, else None.
        """
        try:
            latest_version = self._mlflow_client.get_latest_versions(name=self._name)
        except Exception as e:
            # An odd error when there are no model versions for the given model.
            if (
                "null is not allowed to be used as an element in a repeated field at Response.model_versions"
                in str(e)
            ):  # noqa: E501
                return None
            raise e
        if not latest_version or len(latest_version) < 1:
            return None

        return model_version.ModelVersion.from_mlflow_model_version(latest_version[0])

    def get_experiment(self) -> Optional[Experiment]:
        """
        Get the default experiment associated to the current model.

        Returns:
            Optional[Experiment]: The default experiment associated with the model, or None if not found.
        """
        return get_experiment(f"[model]{self._name}")


def create_model(name: str, description: Optional[str] = None) -> Model:
    """
    Create a new model with the given name and optional tags.
    Args:
        name (str): The name of the model to create.
        description (Optional[str], optional): A description of the model. Defaults to None.
    Returns:
        model.Model: The newly created Model object.
    """
    client = MlflowClient()
    try:
        client.create_registered_model(name=name, description=description)
    except Exception as e:
        process_exception(e)
        raise
    return Model(name=name, description=description)


def get_model(name: str) -> Optional[Model]:
    """
    Fetch an existing model by its name.
    Args:
        name (str): The name of the model to fetch.
    Returns:
        Optional[model.Model]: The fetched Model object if found, or None if not found.
    """
    client = MlflowClient()
    try:
        model = client.get_registered_model(name=name)
        if not model:
            return None
        return Model(
            name=model.name,
            description=model.description if model.description else None,
            mlflow_client=client,
        )
    except Exception as e:
        # Suppress not found errors
        if "RESOURCE_DOES_NOT_EXIST" in str(e):
            return None
        process_exception(e)
        raise
