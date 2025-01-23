import click
from .commands.init import init
from .commands.train import train
from .commands.monitor import monitor
from .commands.deploy import deploy
from .commands.plugins import plugins
from .commands.mlflow import mlflow_cli


@click.group()
def cli():
    """MLOPTIFLOW CLI"""
    pass


cli.add_command(init)
cli.add_command(train)
cli.add_command(deploy)
cli.add_command(monitor)
cli.add_command(plugins)
cli.add_command(mlflow_cli)
