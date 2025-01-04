"""Metadata file and item representation."""

from pydantic import BaseModel


class Item(BaseModel):
    """Single metadata item"""

    value: str
    label: str | None = None
    description: str | None = None
    comment: str | None = None
    image: str | None = None
    link: str | None = None


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
