"""extract pipeline-logs command"""

import os
import re
from typing import TYPE_CHECKING

import click
from click._compat import strip_ansi
from gitlab import Gitlab, GitlabError

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item

if TYPE_CHECKING:
    from gitlab.v4.objects import (
        Project,
        ProjectJob,
        ProjectPipeline,
    )

DEFAULT_REGEX = '^__metadata__:.*key="(?P<key>[a-z_-]+)".*value="(?P<value>[^"]+)"'


def get_project_id(ctx: click.core.Context, param: click.Option, value: int | None) -> int:  # noqa: ARG001
    """Use Project ID from CI_PROJECT_ID if not given."""
    app: ApplicationContext = ctx.obj
    if not value:
        if not os.environ.get("CI_PROJECT_ID"):
            raise click.UsageError(
                "Either use the --project option or set the CI_PROJECT_ID environment variable."
            )
        value = int(str(os.environ.get("CI_PROJECT_ID")))
    app.echo_debug(f"Project ID: {value}")
    return value


def get_pipeline_id(ctx: click.core.Context, param: click.Option, value: int | None) -> int:  # noqa: ARG001
    """Use Pipeline ID from CI_PIPELINE_ID if not given."""
    app: ApplicationContext = ctx.obj
    if not value:
        if not os.environ.get("CI_PIPELINE_ID"):
            raise click.UsageError(
                "Either use the --pipeline option or set the CI_PIPELINE_ID environment variable."
            )
        value = int(str(os.environ.get("CI_PIPELINE_ID")))
    app.echo_debug(f"Pipeline ID: {value}")
    return value


@click.command(name="pipeline-logs")
@click.option(
    "--url",
    default="https://gitlab.com",
    show_default=True,
    help="The Gitlab URL which you would like to connect to.",
)
@click.option("--pat", help="The personal access token used to authenticate.", required=True)
@click.option(
    "--project",
    "project_id",
    type=click.INT,
    help="The project ID of the pipeline you want to collect metadata from. "
    "The value is used from the CI_PROJECT_ID environment if available.",
    callback=get_project_id,
)
@click.option(
    "--pipeline",
    "pipeline_id",
    type=click.INT,
    help="The pipeline ID of the pipeline you want to collect metadata from. "
    "The value is used from the CI_PIPELINE_ID environment if available.",
    callback=get_pipeline_id,
)
@click.option(
    "--regex",
    help="The regular expression to extract the metadata from a single log line.",
    default=DEFAULT_REGEX,
    show_default=True,
)
@click.option(
    "--replace",
    is_flag=True,
    show_default=True,
    help="Replace items in case they already exists.",
)
@click.pass_obj
def pipeline_logs_command(  # noqa: PLR0913
    app: ApplicationContext,
    url: str,
    pat: str,
    project_id: int,
    pipeline_id: int,
    regex: str,
    replace: bool,
) -> None:
    """Extract metadata from gitlab pipeline job logs."""
    try:
        gitlab = Gitlab(url=url, private_token=pat)
        if pat:
            gitlab.auth()
        project: Project = gitlab.projects.get(id=project_id)
        pipeline: ProjectPipeline = project.pipelines.get(id=pipeline_id)
    except GitlabError as error:
        raise click.UsageError(f"{error.error_message} (Gitlab Error)") from error

    for _ in pipeline.jobs.list(iterator=True):
        job: ProjectJob = project.jobs.get(id=_.get_id())
        trace_bytes: bytes = job.trace()  # type: ignore[assignment]
        trace = [strip_ansi(line) for line in trace_bytes.decode(encoding="UTF-8").splitlines()]

        app.echo_info(f"Processing logs of job {job.name}")
        for line in trace:
            app.echo_debug(line)
            match = re.search(regex, line)
            if match and match.group("key") and match.group("value"):
                new_item = Item(value=match.group("value"))
                app.add_item(key=match.group("key"), item=new_item, replace=replace)
