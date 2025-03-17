"""cli"""

import click

from cimd.classes import context
from cimd.commands import add, delete, get, list
from cimd.commands.extend import gitlab_link
from cimd.commands.extract import pipeline_logs, trivy_scans


@click.group(context_settings={"auto_envvar_prefix": "CIMD", "help_option_names": ["-h", "--help"]})
@click.option(
    "--file",
    "-f",
    help="The used metadata JSON file.",
    default="__metadata__.json",
    show_default=True,
)
@click.option("--debug", "-d", is_flag=True, help="Enable output of debug information.")
@click.pass_context
def cli(ctx: click.core.Context, file: str, debug: bool) -> None:
    """Continuous Integration MetaData Command Line Interface

    This tool allows for creation and extension of __metadata__.json
    documents as described on https://github.com/seebi/cimd
    """
    ctx.obj = context.ApplicationContext(filename=file, debug=debug)


@click.group(name="extract")
def extract_group() -> click.Group:  # type: ignore[empty-body]
    """Scrape and collect metadata from sources."""


@click.group(name="extend")
def extend_group() -> click.Group:  # type: ignore[empty-body]
    """Extend metadata items with custom data."""


extend_group.add_command(gitlab_link.gitlab_link_command)
cli.add_command(extend_group)

extract_group.add_command(pipeline_logs.pipeline_logs_command)
extract_group.add_command(trivy_scans.trivy_scan_command)
cli.add_command(extract_group)

cli.add_command(add.add_command)
cli.add_command(delete.delete_command)
cli.add_command(get.get_command)
cli.add_command(list.list_command)
