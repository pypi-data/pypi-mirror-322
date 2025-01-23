from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pathlib import Path
import mlflow


class MLflowTrackingMixin(ABC):
    def __init__(
        self,
        tracking_uri: Optional[str] = None,
        experiment_name: Optional[str] = None,
        artifact_location: Optional[str] = None,
    ):
        self.tracking_uri = tracking_uri or "sqlite:///mlflow.db"
        self.experiment_name = experiment_name or "default"
        self.artifact_location = artifact_location

        Path(self.artifact_location).mkdir(parents=True, exist_ok=True)
        mlflow.set_tracking_uri(self.tracking_uri)

        try:
            experiment_id = mlflow.create_experiment(
                name=self.experiment_name, artifact_location=self.artifact_location
            )
            self.experiment = mlflow.get_experiment(experiment_id)
        except Exception:
            self.experiment = mlflow.get_experiment_by_name(self.experiment_name)

    def start_run(
        self, run_name: Optional[str] = None, nested: bool = False
    ) -> mlflow.ActiveRun:
        return mlflow.start_run(
            experiment_id=self.experiment.experiment_id,
            run_name=run_name,
            nested=nested,
        )

    @abstractmethod
    def log_params(self, params: Dict[str, Any]) -> None:
        """Log parameters to MLflow"""
        pass

    @abstractmethod
    def log_metrics(self, metrics: Dict[str, float]) -> None:
        """Log metrics to MLflow"""
        pass

    @abstractmethod
    def log_model(self, model: Any, artifact_path: str) -> None:
        """Log model to MLflow"""
        pass

    @property
    def X_train(self):
        return self._X_train

    @X_train.setter
    def X_train(self, value):
        self._X_train = value
