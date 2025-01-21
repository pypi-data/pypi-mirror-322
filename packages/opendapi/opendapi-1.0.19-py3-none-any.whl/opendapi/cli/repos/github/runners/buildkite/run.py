"""
CLI for generating, validating and enriching DAPI files: `opendapi github buildkite run`
"""

# pylint: disable=duplicate-code

import os

import click

from opendapi.cli.context_agnostic import RunCommand, repo_runner_run_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.options import (
    dapi_server_options,
    dev_options,
    git_options,
    minimal_schema_options,
    opendapi_run_options,
    third_party_options,
)
from opendapi.cli.repos.github.options import repo_options
from opendapi.cli.repos.github.runners.buildkite.enrich import cli as enrich_cli
from opendapi.cli.repos.github.runners.buildkite.options import runner_options
from opendapi.cli.repos.github.runners.buildkite.register import cli as register_cli


def _should_skip_dbt_cloud__pr(**kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if pull request event and the run is the first attempt
    """
    should_wait_on_dbt_cloud = kwargs.get("dbt_cloud_url") is not None
    # retry of 0 is first run
    run_attempt = (
        int(kwargs.get("buildkite_retry_count"))
        if kwargs.get("buildkite_retry_count")
        else 0
    ) + 1
    # NOTE see if there is another way to get this
    is_pr_event = bool(kwargs["buildkite_pull_request"])

    return should_wait_on_dbt_cloud and is_pr_event and run_attempt == 1


def _should_skip_dbt_cloud__push(**kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if push event - since DBT cloud doesnt run on pushes to main by default
    """
    should_wait_on_dbt_cloud = kwargs.get("dbt_cloud_url") is not None
    # NOTE see if there is another way to get this
    is_push_event = not bool(kwargs["buildkite_pull_request"])

    if should_wait_on_dbt_cloud and is_push_event:
        # HACK: informs DbtDapiValidator
        os.environ["ALWAYS_SKIP_DBT_SYNC"] = "true"
        return True

    return False


def _should_skip_dbt_cloud__all(**kwargs):
    """
    Check if the `generate` command should be skipped

    Skip scenarios:
    1. If integrated with dbt Cloud
        a. Skip if the event is a pull request or push event
    """
    return _should_skip_dbt_cloud__pr(**kwargs) or _should_skip_dbt_cloud__push(
        **kwargs
    )


@click.command()
# common options
@dapi_server_options
@dev_options
@git_options
@minimal_schema_options
@opendapi_run_options
@third_party_options
# github repo options
@repo_options
# github repo bk runner options
@runner_options
def cli(**kwargs):
    """
    This command combines the `generate`, `enrich`, and `register` commands
    conditionally for a Github remote repo running on a Buildkite hosted runner.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """

    # Run register last to ensure the DAPI files are registered and unregistered
    # Register will also validate the DAPI files in the backend
    commands = {
        "generate": RunCommand(
            command=generate_cli,
            description="generate DAPI files",
            skip_condition=_should_skip_dbt_cloud__all,
        ),
        "enrich": RunCommand(
            command=enrich_cli,
            description="validate and enrich DAPI files",
            skip_condition=_should_skip_dbt_cloud__all,
        ),
        "register": RunCommand(
            command=register_cli,
            description="register DAPI files",
            skip_condition=None,
        ),
    }

    repo_runner_run_cli(commands, kwargs)
