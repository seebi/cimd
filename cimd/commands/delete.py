"""delete command"""

import click

from cimd.classes.context import ApplicationContext


@click.command(name="delete")
@click.argument("KEY")
@click.pass_obj
def delete_command(
    app: ApplicationContext,
    key: str,
) -> None:
    """Delete a metadata item."""
    app.delete_item(key=key)
