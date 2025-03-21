"""gitlab-link command"""

import os

import click

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import ITEM_FIELDS


def get_job_url(ctx: click.core.Context, param: click.Option, value: str | None) -> str:  # noqa: ARG001
    """Use Job URL from CI_JOB_URL if not given."""
    app: ApplicationContext = ctx.obj
    if not value:
        if not os.environ.get("CI_JOB_URL"):
            raise click.UsageError(
                "Either use the --job option or set the CI_JOB_URL environment variable."
            )
        value = os.environ.get("CI_JOB_URL", "")
    value = value.strip("/")
    app.echo_debug(f"Job URL: {value}")
    return value


@click.command(name="gitlab-link")
@click.argument(
    "PATTERN",
)
@click.option(
    "--field",
    type=click.Choice(ITEM_FIELDS),
    default="key",
    help="On which field the pattern has to match.",
)
@click.option(
    "--job-url",
    "job_url",
    help="The job URL of the gitlab pipeline job which created the file. "
    "The value is used from the CI_JOB_URL environment if available.",
    callback=get_job_url,
)
@click.option(
    "--artifact-path",
    "artifact_path",
    help="The relative path to your artifact file. This file needs to be "
    "part of the exported job artifacts.",
    required=True,
)
@click.pass_obj
def gitlab_link_command(
    app: ApplicationContext, pattern: str, field: str, job_url: str, artifact_path: str
) -> None:
    """Extend metadata items with a raw gitlab artifact link.

    To select the items you want to extend, a pattern + an optional field can be used.
    """
    artifact_path = artifact_path.strip("/")
    for key, item in app.file.get_filtered_items(pattern=pattern, field=field).items():
        item.link = f"{job_url}/artifacts/raw/{artifact_path}"
        app.add_item(key=key, item=item, replace=True)
