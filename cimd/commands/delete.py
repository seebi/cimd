"""delete command"""

import click

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import ITEM_FIELDS


@click.command(name="delete")
@click.argument(
    "PATTERN",
)
@click.option(
    "--field",
    type=click.Choice(ITEM_FIELDS),
    default="key",
    help="On which field the pattern has to match.",
)
@click.pass_obj
def delete_command(
    app: ApplicationContext,
    pattern: str,
    field: str,
) -> None:
    """Delete metadata items.

    This command deletes metadata items based on a regular expression.
    This regular expression needs to fully match a key
    (or optionally another field) in order to delete the item.
    """
    for key in app.file.get_filtered_items(pattern=pattern, field=field):
        app.delete_item(key=key)
