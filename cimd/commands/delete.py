"""delete command"""

import click

from cimd.callbacks import filter_items_with_expression
from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item


@click.command(name="delete")
@click.argument(
    "KEY_EXPRESSION",
    callback=filter_items_with_expression,
)
@click.pass_obj
def delete_command(
    app: ApplicationContext,
    key_expression: dict[str, Item],
) -> None:
    """Delete metadata items.

    This command deletes metadata items based on a key-expression.
    This regular expression needs to fully match a key in order to delete the item.
    """
    filtered_items = key_expression  # click does not allow aliases for arguments
    if len(filtered_items) == 0:
        raise click.UsageError("No items matching this expression.")
    for key in filtered_items:
        app.delete_item(key=key)
