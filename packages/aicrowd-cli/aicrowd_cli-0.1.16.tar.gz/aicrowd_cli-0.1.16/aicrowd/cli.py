#!/usr/bin/env python

"""
Entrypoint for the CLI application
"""

import logging

import click
from rich import traceback
from rich.logging import RichHandler

from aicrowd.cmd import (
    challenge_command,
    config_command,
    dataset_command,
    login_command,
    notebook_command,
    submission_command,
    version_command,
)
from aicrowd.contexts import ConfigContext, pass_config
from aicrowd.utils import AliasedGroup
from aicrowd.utils.utils import check_for_latest_version

traceback.install()

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


# pylint: disable=no-value-for-parameter
@click.group(cls=AliasedGroup)
@click.option("-v", "--verbose", count=True, help="Enable verbose output.")
@click.option("--config-path", help="Path to config file", type=click.Path())
@pass_config
def cli(
    config_context: ConfigContext,
    verbose: int,
    config_path: str,
):
    """
    AIcrowd CLI
    """
    if verbose > 0:
        level = LOGGING_LEVELS[verbose] if verbose in LOGGING_LEVELS else logging.DEBUG
    else:
        level = logging.CRITICAL

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(show_path=False, show_time=False)],
    )

    # load config from path
    config_context.config.load(config_path)

    if not config_context.config.get("disable_update_check"):
        check_for_latest_version()


cli.add_command(challenge_command)
cli.add_command(dataset_command)
cli.add_command(login_command)
cli.add_command(submission_command)
cli.add_command(version_command)
cli.add_command(notebook_command)
cli.add_command(config_command)


if __name__ == "__main__":
    cli()
