"""Context object for the CLI"""

import json
from datetime import UTC, datetime
from os import getenv
from pathlib import Path

import click
from click import UsageError
from rich import box
from rich.console import Console
from rich.table import Table

from cimd.classes.metadata import File, Item


class ApplicationContext:
    """Context object for the CLI"""

    def __init__(self, filename: str, debug: bool):
        self.debug = debug
        self.filename = Path(filename)
        self.file: File = self.load_file()
        self.console = Console()
        console_width = getenv("CIMD_CONSOLE_WIDTH", None)
        if console_width is not None:
            self.console.width = int(console_width)

    def echo_debug(self, message: str) -> None:
        """Output a debug message if --debug is enabled."""
        # pylint: disable=invalid-name
        if self.debug:
            now = datetime.now(tz=UTC)
            click.secho(f"[{now!s}] {message}", err=True, dim=True)

    @staticmethod
    def echo_info(message: str, nl: bool = True, fg: str = "") -> None:
        """Output an info message"""
        click.secho(message, nl=nl, fg=fg)

    def echo_info_table(
        self, rows: list, headers: list[str], sort_column: int | None = None
    ) -> None:
        """Output a formatted and highlighted table as info message."""
        table = Table(
            box=box.HEAVY,
            row_styles=["bold", ""],
            header_style="Yellow",
            border_style="Yellow",
            show_lines=True,
        )
        for header in headers:
            table.add_column(header)
        if sort_column is not None:
            rows = sorted(rows, key=lambda k: k[sort_column].lower())
        for row in rows:
            table.add_row(*row)
        self.console.print(table)

    def load_file(self) -> File:
        """Load metadata from path"""
        if not self.filename.exists():
            self.filename.write_text(File().model_dump_json(exclude_none=True, indent=2))
        with self.filename.open("r") as file_reader:
            content = json.load(file_reader)
            return File(**content)

    def save_file(self) -> None:
        """Save metadata to JSON"""
        with Path(self.filename).open("w") as file:
            file.write(self.file.model_dump_json(exclude_none=True, indent=2))

    def add_item(self, key: str, item: Item, replace: bool = False) -> None:
        """Add an item and save"""
        method = "REPLACE" if replace and key in self.file.items else "ADD"
        self.echo_debug(f"{method} {item}")
        try:
            self.file.add_item(key=key, item=item, replace=replace)
        except KeyError as error:
            raise UsageError(
                f"Item with key '{key}' already exists in file '{self.filename}'"
            ) from error
        self.save_file()
        self.echo_info(f"{method}: {key} ({item.value})")

    def delete_item(self, key: str) -> None:
        """Delete an item and save"""
        try:
            self.file.delete_item(key=key)
        except KeyError as error:
            raise UsageError(
                f"Item with key '{key}' does not exist in file '{self.filename}'"
            ) from error
        self.save_file()
        self.echo_info(f"DELETE: {key}")

    def get_item(self, key: str) -> Item:
        """Get an item"""
        if key not in self.file.items:
            raise UsageError(f"Item with key '{key}' does not exist in file '{self.filename}'")
        return self.file.items[key]
