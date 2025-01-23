from typing import Any, Dict
import mlflow
from .base import MLflowTrackingMixin


class TabularMLflowTracking(MLflowTrackingMixin):
    def log_params(self, params: Dict[str, Any]) -> None:
        mlflow.log_params(params)

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        mlflow.log_metrics(metrics)

    def log_model(self, model: Any, artifact_path: str) -> None:
        mlflow.sklearn.log_model(model, artifact_path)
