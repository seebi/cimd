"""validate command"""

import click

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
    table = []
    if keys_only:
        for key in app.file.items:
            app.echo_info(key)
        return

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
