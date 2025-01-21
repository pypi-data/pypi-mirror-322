"""
Houses common functionality for running OpenDapi
functions - independent of repo/runner.
"""

from collections import namedtuple
from typing import Dict, Optional, Type

import click

from opendapi.adapters.dapi_server import DAPIChangeNotification, DAPIRequests
from opendapi.adapters.file import OpenDAPIFileContents
from opendapi.adapters.git import ChangeTriggerEvent
from opendapi.cli.common import Schemas, get_opendapi_config_from_root, print_cli_output
from opendapi.cli.enrichers.base import EnricherBase
from opendapi.cli.options import (  # NOTE: see !! IMPORTANT !! note below
    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION,
    CATEGORIES_PARAM_NAME_WITH_OPTION,
    DAPI_PARAM_NAME_WITH_OPTION,
    DATASTORES_PARAM_NAME_WITH_OPTION,
    PURPOSES_PARAM_NAME_WITH_OPTION,
    SUBJECTS_PARAM_NAME_WITH_OPTION,
    TEAMS_PARAM_NAME_WITH_OPTION,
    construct_dapi_server_config,
)
from opendapi.feature_flags import FeatureFlag, set_feature_flags
from opendapi.features import load_from_raw_dict, set_feature_to_status
from opendapi.logging import LogDistKey, Timer, logger, sentry_init

# NOTE think about commenting which common options are used in each command

########## main ##########


def repo_runner_cli(
    change_trigger_event: ChangeTriggerEvent,
    sentry_tags: dict,
    kwargs: dict,
):
    """
    To be used by the 'main' cli for a repo/runner combo, i.e.
    opendapi.cli.repos.github.runners.buildkite.main.cli

    Takes care of getting common information from DapiServer, setting up sentry,
    etc.
    """

    # NOTE: !! IMPORTANT !!
    #       If we include any additional envvar setting here that are options that we expect
    #       subcommands to inherit, we must add them in `opendapi/cli/run` due to the manner in
    #       which it invokes the main_cli during the migration

    dapi_server_config = construct_dapi_server_config(kwargs)
    dapi_requests = None

    BASE_COMMIT_SHA_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
        kwargs, change_trigger_event.before_change_sha
    )

    if not kwargs.get("skip_client_config"):
        try:
            # Initialize sentry and fetch Feature flags
            # This fails silently if the client config is not available
            # This is temporary to monitor if this actually breaks
            dapi_requests = DAPIRequests(
                dapi_server_config=dapi_server_config,
                trigger_event=change_trigger_event,
            )

            client_config = dapi_requests.get_client_config_from_server()
            sentry_tags.update(client_config.get("sentry_tags", {}))
            sentry_init(
                client_config.get("sentry", {}),
                tags=sentry_tags,
            )

            if client_config.get("fetch_feature_flags", False):
                feature_flags: dict = (
                    dapi_requests.get_client_feature_flags_from_server(
                        [f.value for f in FeatureFlag]
                    )
                )
                set_feature_flags(
                    {
                        FeatureFlag(f): val
                        for f, val in feature_flags.items()
                        if FeatureFlag.has_value(f)
                    }
                )
        except Exception as exp:  # pylint: disable=broad-except
            logger.error("Error fetching client config: %s", exp)

    all_params_present = all(
        kwargs.get(param.name) is not None
        for param in (
            CATEGORIES_PARAM_NAME_WITH_OPTION,
            DAPI_PARAM_NAME_WITH_OPTION,
            DATASTORES_PARAM_NAME_WITH_OPTION,
            PURPOSES_PARAM_NAME_WITH_OPTION,
            SUBJECTS_PARAM_NAME_WITH_OPTION,
            TEAMS_PARAM_NAME_WITH_OPTION,
        )
    )
    fetched_repo_features_info = None
    if not all_params_present and not kwargs.get("skip_server_minimal_schemas"):
        # we do not try/catch here, since if they are not set to skipped then they are required
        # for the run
        dapi_requests = dapi_requests or DAPIRequests(
            dapi_server_config=dapi_server_config,
            trigger_event=change_trigger_event,
        )
        fetched_repo_features_info = dapi_requests.get_repo_features_info_from_server()
        enabled_schemas = fetched_repo_features_info.enabled_schemas
        CATEGORIES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.categories
        )
        DAPI_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(kwargs, enabled_schemas.dapi)
        DATASTORES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.datastores
        )
        PURPOSES_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.purposes
        )
        SUBJECTS_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.subjects
        )
        TEAMS_PARAM_NAME_WITH_OPTION.set_as_envvar_if_none(
            kwargs, enabled_schemas.teams
        )

    raw_feature_to_status = kwargs.get("feature_to_status")
    # not set, load from dapi server
    if raw_feature_to_status is None:
        if not fetched_repo_features_info:
            dapi_requests = dapi_requests or DAPIRequests(
                dapi_server_config=dapi_server_config,
                trigger_event=change_trigger_event,
            )
            fetched_repo_features_info = (
                dapi_requests.get_repo_features_info_from_server()
            )

        feature_to_status = fetched_repo_features_info.feature_to_status

    # set, load from env var raw dict
    else:
        feature_to_status = load_from_raw_dict(raw_feature_to_status)

    set_feature_to_status(feature_to_status)


########## enrich ##########


def repo_runner_enrich_cli(
    change_trigger_event: ChangeTriggerEvent,
    enricher_cls: Type[EnricherBase],
    metrics_tags: dict,
    markdown_file: Optional[str],
    kwargs: dict,
):
    """
    To be used by the 'enrich' cli for a repo/runner combo, i.e.
    opendapi.cli.repos.github.runners.buildkite.enrich.cli

    Actually invokes the enricher class to enrich generated Dapi files.
    """
    opendapi_config = get_opendapi_config_from_root(kwargs.get("local_spec_path"))
    dapi_server_config = construct_dapi_server_config(kwargs)
    minimal_schemas = Schemas(
        teams=TEAMS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        datastores=DATASTORES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        purposes=PURPOSES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        dapi=DAPI_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        subjects=SUBJECTS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        categories=CATEGORIES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
    )
    enricher = enricher_cls(
        config=opendapi_config,
        dapi_server_config=dapi_server_config,
        trigger_event=change_trigger_event,
        revalidate_all_files=dapi_server_config.revalidate_all_files,
        require_committed_changes=dapi_server_config.require_committed_changes,
        minimal_schemas_for_validation=minimal_schemas,
        markdown_file=markdown_file,
    )

    enricher.print_markdown_and_text(
        "\nGetting ready to validate and enrich your DAPI files...",
        color="green",
    )
    with Timer(dist_key=LogDistKey.CLI_ENRICH, tags=metrics_tags):
        enricher.run()


########## register ##########


def repo_runner_register_cli(
    change_trigger_event: ChangeTriggerEvent,
    markdown_file: Optional[str],
    kwargs: dict,
):
    """
    To be used by the 'register' cli for a repo/runner combo, i.e.
    opendapi.cli.repos.github.runners.buildkite.register.cli

    Registers Dapi files with the Dapi server.
    """
    opendapi_config = get_opendapi_config_from_root(kwargs.get("local_spec_path"))
    dapi_server_config = construct_dapi_server_config(kwargs)
    minimal_schemas = Schemas(
        teams=TEAMS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        datastores=DATASTORES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        purposes=PURPOSES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        dapi=DAPI_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        subjects=SUBJECTS_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
        categories=CATEGORIES_PARAM_NAME_WITH_OPTION.extract_from_kwargs(kwargs),
    )
    dapi_requests = DAPIRequests(
        dapi_server_config=dapi_server_config,
        trigger_event=change_trigger_event,
        opendapi_config=opendapi_config,
        error_msg_handler=lambda msg: print_cli_output(
            msg,
            color="red",
            bold=True,
            markdown_file=markdown_file,
        ),
        error_exception_cls=click.ClickException,
        txt_msg_handler=lambda msg: print_cli_output(
            msg,
            color="yellow",
            bold=True,
            no_markdown=True,
        ),
        markdown_msg_handler=lambda msg: print_cli_output(
            msg,
            color="yellow",
            bold=True,
            markdown_file=markdown_file,
            no_text=True,
        ),
    )

    should_register = (
        dapi_server_config.register_on_merge_to_mainline
        and (
            change_trigger_event.where == "local"
            or (
                change_trigger_event.where == "github"
                and change_trigger_event.is_push_event
                and change_trigger_event.git_ref
                == f"refs/heads/{dapi_server_config.mainline_branch_name}"
            )
        )
        and (dapi_server_config.woven_integration_mode != "disabled")
    )

    metrics_tags = {
        "org_name": opendapi_config.org_name_snakecase,
        "where": change_trigger_event.where,
        "event_type": change_trigger_event.event_type,
        "should_register": should_register,
    }

    if not should_register:
        print_cli_output(
            "Skipping opendapi register command",
            color="yellow",
            bold=True,
        )
        return

    with Timer(dist_key=LogDistKey.CLI_REGISTER, tags=metrics_tags):
        all_files = OpenDAPIFileContents.build_from_all_files(opendapi_config)

        current_commit_files = OpenDAPIFileContents.build_from_all_files_at_commit(
            opendapi_config, change_trigger_event.after_change_sha
        )

        print_cli_output(
            f"Registering {len(all_files)} DAPI files with the DAPI server...",
            color="green",
            bold=True,
            markdown_file=markdown_file,
        )

        with click.progressbar(length=len(all_files.dapis)) as progressbar:
            register_result = dapi_requests.register(
                all_files=all_files,
                onboarded_files=current_commit_files,
                commit_hash=change_trigger_event.after_change_sha,
                source=opendapi_config.urn,
                notify_function=lambda progress: progressbar.update(progress)
                or print_cli_output(
                    f"Finished {round(progressbar.pct * 100)}% "
                    f"with {progressbar.format_eta()} remaining",
                    color="green",
                    markdown_file=markdown_file,
                ),
                minimal_schemas_for_validation=minimal_schemas,
            )

            # unregister missing dapis
            unregister_result = dapi_requests.unregister(
                source=opendapi_config.urn,
                except_dapi_urns=[dapi["urn"] for dapi in all_files.dapis.values()],
            )

            # send notifications
            total_change_notification = (
                DAPIChangeNotification.safe_merge(
                    register_result.dapi_change_notification,
                    unregister_result.dapi_change_notification,
                )
                or DAPIChangeNotification()
            )
            dapi_requests.notify(total_change_notification)

        print_cli_output(
            "Successfully registered DAPI files with the DAPI server",
            color="green",
            bold=True,
            markdown_file=markdown_file,
        )


########## run ##########

RunCommand = namedtuple("RunCommand", ["command", "description", "skip_condition"])


def repo_runner_run_cli(
    commands: Dict[str, RunCommand],
    kwargs: dict,
):
    """
    To be used by the 'run' cli for a repo/runner combo, i.e.
    opendapi.cli.repos.github.runners.buildkite.run.cli

    Given a set of commands, runs then as long as they are not intended to be skipped
    (i.e. a third party integration may not be ready to have generate run yet)
    """
    for command_name, command_info in commands.items():
        if command_info.skip_condition and command_info.skip_condition(**kwargs):
            print_cli_output(
                f"Skipping {command_info.description} command",
                color="yellow",
                bold=True,
            )
            continue

        print_cli_output(
            f"Running `opendapi {command_name}` to {command_info.description}...",
            color="green",
            bold=True,
        )
        command = command_info.command
        command_params = command.params
        # run's params should always be a superset of all the children's params,
        # and therefore we do unsafe dict access as to not swallow any discrepancies
        command_kwargs = {key.name: kwargs[key.name] for key in command_params}
        with click.Context(command) as ctx:
            ctx.invoke(command, **command_kwargs)
