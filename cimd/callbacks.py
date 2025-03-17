"""Shared click parameter and option callback functions"""

import re
from typing import TYPE_CHECKING

import click

from cimd.classes.metadata import Item

if TYPE_CHECKING:
    from cimd.classes.context import ApplicationContext


def filter_items_with_expression(
    ctx: click.core.Context,
    param: click.Option,  # noqa: ARG001
    value: str,
) -> dict[str, Item]:
    """Process a key expression and return a dict of items"""
    try:
        expression = re.compile(value)
    except re.error as error:
        raise click.UsageError(f"Invalid regular expression - {error!s}") from error

    app: ApplicationContext = ctx.obj
    filtered_items: dict[str, Item] = {}
    for key in app.file.items:
        if expression.fullmatch(key):
            app.echo_debug(f"Key '{key}' matches '{value}'")
            filtered_items[key] = app.get_item(key)
        else:
            app.echo_debug(f"Key '{key}' does not match '{value}'")
    return filtered_items
