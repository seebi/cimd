"""cli"""

import click

from cimd.classes import context
from cimd.commands import add, delete, get, list
from cimd.commands.scratch import pipeline_logs


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


@click.group(name="scratch")
def scratch_group() -> click.Group:  # type: ignore[empty-body]
    """Collect and add metadata from sources."""


scratch_group.add_command(pipeline_logs.pipeline_logs_command)

cli.add_command(add.add_command)
cli.add_command(delete.delete_command)
cli.add_command(get.get_command)
cli.add_command(list.list_command)
cli.add_command(scratch_group)
