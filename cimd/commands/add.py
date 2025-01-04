"""add command"""

import click

from cimd.classes import metadata
from cimd.classes.context import ApplicationContext


@click.command(name="add")
@click.argument("KEY")
@click.argument("VALUE")
@click.option(
    "--label",
    help="Provide an optional label.",
)
@click.option(
    "--description",
    help="Provide an optional description.",
)
@click.option(
    "--comment",
    help="Provide an optional comment.",
)
@click.option(
    "--image",
    help="Provide an optional image URL.",
)
@click.option(
    "--link",
    help="Provide an optional link URL.",
)
@click.option(
    "--replace",
    is_flag=True,
    show_default=True,
    help="Replace the item in case it already exists.",
)
@click.pass_obj
def add_command(  # noqa: PLR0913
    app: ApplicationContext,
    key: str,
    value: str,
    label: str,
    description: str,
    comment: str,
    image: str,
    link: str,
    replace: bool,
) -> None:
    """Add a metadata item."""
    item = metadata.Item(value=value)
    if label:
        item.label = label
    if description:
        item.description = description
    if comment:
        item.comment = comment
    if image:
        item.image = image
    if link:
        item.link = link
    app.add_item(key=key, item=item, replace=replace)
