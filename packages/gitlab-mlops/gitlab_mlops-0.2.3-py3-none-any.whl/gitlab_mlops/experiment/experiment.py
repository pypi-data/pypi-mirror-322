from typing import Any, Optional

import mlflow

import gitlab_mlops.experiment.run as run
from gitlab_mlops.mlflow.exceptions import process_exception


class Experiment:
    """
    Represents the details of an MLflow experiment, including its ID, name and associated tags.
    """

    def __init__(
        self, experiment_id: str, name: str, tags: Optional[dict[str, Any]] = None
    ):
        """
        Args:
            experiment_id (str): The unique identifier of the experiment.
            name (str): The name of the experiment.
            tags (Optional[dict[str, Any]], optional): A dictionary of tags associated with the experiment. Defaults to None.
        """
        self._id = experiment_id
        self._name = name
        self._tags = tags

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def tags(self) -> dict[str, Any] | None:
        return self._tags

    def create_run(self) -> run.Run:
        """
        Create a new (candidate) run within this experiment.

        Returns:
            Run: A new Run instance representing the created run.
        """
        return run.create_run(experiment_id=self._id)


def create_experiment(name: str, tags: Optional[dict[str, Any]] = None) -> Experiment:
    """
    Create a new MLflow experiment.

    Args:
        name (str): The name of the new experiment.
        tags (Optional[dict[str, Any]], optional): A dictionary of tags to associate with the experiment. Defaults to None.

    Returns:
        Experiment: An Experiment instance representing the newly created experiment.
    """
    try:
        experiment_id = mlflow.create_experiment(name=name, tags=tags)
        return Experiment(experiment_id=experiment_id, name=name, tags=tags)
    except Exception as e:
        process_exception(e)
        raise


def get_experiment(name: str) -> Optional[Experiment]:
    """
    Retrieve an existing MLflow experiment by name.

    Args:
        name (str): The name of the experiment to retrieve.

    Returns:
        Optional[Experiment]: An Experiment instance if found, None if no experiment with the given name exists.
    """
    try:
        experiment = mlflow.get_experiment_by_name(name=name)
        if experiment:
            return Experiment(
                experiment_id=str(experiment.experiment_id),
                name=experiment.name,
                tags=experiment.tags if experiment.tags else None,
            )
        return None
    except Exception as e:
        process_exception(e)
        raise
