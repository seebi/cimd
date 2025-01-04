"""validate command"""

import click

from cimd.classes import context


@click.command(name="list")
@click.pass_obj
def list_command(app: context.ApplicationContext) -> None:
    """List metadata items."""
    table = []
    for key, item in app.file.items.items():
        row = [key, item.value]
        addons = ""
        for addon_key, addon_value in item.model_dump(exclude_none=True).items():
            if addon_key == "value":
                continue
            addons += f"{addon_key}: {addon_value}\n"

        row.append(addons)
        table.append(row)
    app.echo_info_table(table, headers=["Key", "Value", "Additional Fields"], sort_column=0)
