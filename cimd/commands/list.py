"""validate command"""

import click
from rich.table import Table

from cimd.classes import context


@click.command(name="list")
@click.option(
    "--keys-only",
    is_flag=True,
    help="Show only item keys.",
)
@click.pass_obj
def list_command(app: context.ApplicationContext, keys_only: bool) -> None:
    """List metadata items."""
    rows = []
    if keys_only:
        for key in app.file.items:
            app.echo_info(key)
        return

    for key, item in app.file.items.items():
        row: list[str | Table] = [key, item.value]
        addons = Table(box=None, padding=(0, 0), show_header=False)

        for addon_key, addon_value in item.model_dump(exclude_none=True).items():
            if addon_key == "value":
                continue
            if addon_key in ("image", "link"):
                addons.add_row(f"{addon_key}: ", f"[link={addon_value}]{addon_value}[/link]")
            else:
                addons.add_row(f"{addon_key}: ", addon_value)

        row.append(addons)
        rows.append(row)
    app.echo_info_table(rows, headers=["Key", "Value", "Optional Fields"], sort_column=0)
