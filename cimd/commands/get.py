"""get command"""

import click
from click import UsageError

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item


@click.command(name="get")
@click.argument("KEY")
@click.argument("TERM", type=click.Choice(list(Item.model_fields)), default="value")
@click.pass_obj
def get_command(app: ApplicationContext, key: str, term: str) -> None:
    """Get data of a metadata item."""
    item = app.get_item(key).model_dump(exclude_none=True)
    if term not in item:
        raise UsageError(f"Item with key '{key}' has no attribute '{term}'")
    app.echo_info(str(item.get(term)))
