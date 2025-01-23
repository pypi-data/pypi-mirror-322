import os
import re
from typing import Any, Optional

from gitlab_mlops import experiment, model
from gitlab_mlops.experiment import Experiment
from gitlab_mlops.experiment.run import Run
from gitlab_mlops.model import Model, ModelVersion

__all__ = ["Client", "TRACKING_URI_ENV", "TRACKING_TOKEN_ENV"]

TRACKING_URI_ENV = "MLFLOW_TRACKING_URI"
TRACKING_TOKEN_ENV = "MLFLOW_TRACKING_TOKEN"

_tracking_uri_regex = r"^https?://[^/]+/api/v4/projects/\d+/ml/mlflow/?$"
_gitlab_token_regex = r"glpat-[0-9a-zA-Z\-]{20}"


class Client:
    """
    A central client for managing GitLab MLOps operations, including experiment tracking,
    metric logging, and model versioning.

    The Client handles authentication, environment variable setup, and provides
    an easy-to-use interface for ML experiment and model management workflows.
    """

    def __init__(
        self, tracking_uri: Optional[str] = None, gitlab_token: Optional[str] = None
    ):
        """
        Args:
            tracking_uri (Optional[str]): The GitLab tracking URI in the following format:
                `<gitlab host name>/api/v4/projects/<gitlab project ID>/ml/mlflow`.
                If not provided, the environment variable `MLFLOW_TRACKING_URI` will be used.
                If neither is set, a ValueError will be raised.
            gitlab_token (Optional[str]): A valid GitLab token for the project associated with
                the tracking URI. The token must have at least the Developer role and include
                the `api` permission. If not provided, the environment variable `MLFLOW_TRACKING_TOKEN`
                will be used. If neither is set, a ValueError will be raised.
        """
        tracking_uri = self._tracking_uri_or_env(tracking_uri)
        gitlab_token = self._gitlab_token_or_env(gitlab_token)

        self._validate_tracking_uri(tracking_uri)
        self._validate_gitlab_token(gitlab_token)

        self._tracking_uri = tracking_uri
        self._gitlab_token = gitlab_token
        os.environ[TRACKING_URI_ENV] = self._tracking_uri
        os.environ[TRACKING_TOKEN_ENV] = self._gitlab_token

    @staticmethod
    def _tracking_uri_or_env(tracking_uri: Optional[str]) -> str:
        if tracking_uri:
            return tracking_uri

        env_tracking_uri = os.environ.get(TRACKING_URI_ENV)
        if env_tracking_uri:
            return env_tracking_uri

        raise ValueError(
            "Tracking URI cannot be None. Example URI: 'https://gitlab.com/api/v4/projects/<your_project_id>/ml/mlflow'"
        )

    @staticmethod
    def _gitlab_token_or_env(gitlab_token: Optional[str]) -> str:
        if gitlab_token:
            return gitlab_token

        env_gitlab_token = os.environ.get(TRACKING_TOKEN_ENV)
        if env_gitlab_token:
            return env_gitlab_token

        raise ValueError("Gitlab token cannot be None")

    @staticmethod
    def _validate_tracking_uri(tracking_uri: str):
        if not re.match(_tracking_uri_regex, tracking_uri):
            raise ValueError(
                f"The tracking URI '{tracking_uri}' must be in the format '<gitlab host name>/api/v4/projects/<gitlab project ID>/ml/mlflow'"
            )

    @staticmethod
    def _validate_gitlab_token(gitlab_token: str):
        if not re.match(_gitlab_token_regex, gitlab_token):
            raise ValueError(
                f"The Gitlab token '{gitlab_token}' must be in the format 'glpat-XXXXXXXXXXXXXXXXXXXX'"
            )

    def create_experiment(
        self, name: str, tags: Optional[dict[str, Any]] = None
    ) -> Experiment:
        """
        Create a new experiment with the given name and optional tags.

        Args:
            name (str): The name of the experiment to create.
            tags (Optional[dict[str, Any]], optional): A dictionary of tags to associate
                with the experiment. Defaults to None.

        Returns:
            experiment.Experiment: The newly created Experiment object.
        """
        return experiment.create_experiment(
            name=name,
            tags=tags,
        )

    def get_experiment(self, name: str) -> Optional[Experiment]:
        """
        Fetch an existing experiment by its name.

        Args:
            name (str): The name of the experiment to fetch.

        Returns:
            Optional[experiment.Experiment]: The fetched Experiment object if found, or None
                if not found.
        """
        return experiment.get_experiment(name=name)

    def get_run(self, run_id: str) -> Optional[Run]:
        """
        Fetch an existing run by its run_id.
        Args:
            run_id (str): The run_id of the run to fetch.
        Returns:
            Optional[experiment.Run]: The fetched Run object if found, or None if not found.
        """
        return experiment.get_run(run_id=run_id)

    def create_model(self, name: str, description: Optional[str] = None) -> Model:
        """
        Create a new model with the given name and optional tags.:
        Args:
            name (str): The name of the model to create.
            description (Optional[str], optional): A description of the model. Defaults to None.
        Returns:
            model.Model: The newly created Model object.
        """
        return model.create_model(name=name, description=description)

    def get_model(self, name: str) -> Optional[Model]:
        """
        Fetch an existing model by its name.
        Args:
            name (str): The name of the model to fetch.
        Returns:
            Optional[model.Model]: The fetched Model object if found, or None if not found.
        """
        return model.get_model(name=name)

    def get_model_version(
        self, model_name: str, version: str
    ) -> Optional[ModelVersion]:
        """
        Fetch an existing model version by its model name and version.
        Args:
            model_name (str): The name of the model.
            version (str): The SemVer version of the model.
        Returns:
            Optional[model.ModelVersion]: The fetched ModelVersion object if found, or None if not found.
        """
        return model.get_model_version(model_name=model_name, version=version)
