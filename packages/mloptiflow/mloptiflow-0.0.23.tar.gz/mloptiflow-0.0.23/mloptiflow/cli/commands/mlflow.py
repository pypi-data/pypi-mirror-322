import click
import mlflow
import subprocess


@click.group()
def mlflow_cli():
    """MLflow integration commands."""
    pass


@mlflow_cli.command()
def ui():
    """Launch MLflow UI."""
    subprocess.run(["mlflow", "ui"])


@mlflow_cli.command()
@click.option("--run-id", required=True, help="MLflow run ID")
@click.option("--model-name", required=True, help="Name to register the model under")
def register_model(run_id: str, model_name: str):
    """Register a model from a run."""
    model_uri = f"runs:/{run_id}/model"
    mlflow.register_model(model_uri, model_name)
