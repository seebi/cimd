"""Metadata file and item representation."""

import re

import click
from pydantic import BaseModel


class Item(BaseModel):
    """Single metadata item"""

    value: str
    label: str | None = None
    description: str | None = None
    comment: str | None = None
    image: str | None = None
    link: str | None = None


ITEM_FIELDS = ["key", *list(Item.model_fields)]


class File(BaseModel):
    """__metadata__ file"""

    items: dict[str, Item] = {}

    def add_item(self, key: str, item: Item, replace: bool = False) -> None:
        """Add item"""
        if not replace and key in self.items:
            raise KeyError(f"Item with key '{key}' already in metadata file.")
        self.items[key] = item

    def delete_item(self, key: str) -> None:
        """Delete item"""
        del self.items[key]

    def get_filtered_items(
        self, pattern: str, field: str, error_on_empty: bool = True
    ) -> dict[str, Item]:
        """Return a filtered dict of items"""
        field = field.lower()
        try:
            expression = re.compile(pattern=pattern)
        except re.error as error:
            raise click.UsageError(f"Invalid regular expression - {error!s}") from error

        filtered_items: dict[str, Item] = {}
        for key, item in self.items.items():
            value = None
            if field == "key":
                value = key
            if field in Item.model_fields:
                value = getattr(item, field)
            if value is None:
                raise click.UsageError(f"Unknown field '{field}'.")
            if expression.fullmatch(value):
                filtered_items[key] = self.items[key]

        if error_on_empty and len(filtered_items) == 0:
            raise click.UsageError(f"No items matching '{field} ~= {pattern}'.")

        return filtered_items
