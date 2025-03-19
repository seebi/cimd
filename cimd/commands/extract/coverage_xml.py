"""coverage-xml command"""

import click
from defusedxml.ElementTree import ParseError, parse

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item
from cimd.classes.shields_link import ShieldsLink

BEST_THRESHOLD = 90
GOOD_THRESHOLD = 75
MEDIUM_THRESHOLD = 50


def image_for_line_rate_item(line_rate: float) -> ShieldsLink:
    """Create a shields.io image for a junit key

    same colors as in genbadge project:
    https://github.com/smarie/python-genbadge/blob/main/genbadge/utils_coverage.py#L105C1-L119C17
    """
    if line_rate < MEDIUM_THRESHOLD:
        color = "red"
    elif line_rate < GOOD_THRESHOLD:
        color = "orange"
    elif line_rate < BEST_THRESHOLD:
        color = "green"
    else:
        color = "brightgreen"
    return ShieldsLink(label="Coverage", message=f"{line_rate!s}%", color=color)


@click.command(name="coverage-xml")
@click.argument(
    "XML_FILE",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace items in case they already exists.",
)
@click.pass_obj
def coverage_xml_command(app: ApplicationContext, xml_file: str, replace: bool) -> None:
    """Extract metadata from a Coverage XML output files.

    This command will extract code coverage percentage.
    """
    try:
        xml = parse(xml_file)
        app.echo_debug(f"{xml_file} parsed")
    except ParseError as error:
        raise click.UsageError(f"{xml_file} - {error!s}") from error
    root = xml.getroot()
    line_rate: float = round(float(root.attrib.get("line-rate")) * 100, ndigits=2)
    key = "coverage-py-line-rate"
    new_item = Item(
        value=str(line_rate),
        label="Coverage",
        description="Overall coverage percentage (line-rate)",
        image=image_for_line_rate_item(line_rate=line_rate).to_string(),
    )
    app.add_item(key=key, item=new_item, replace=replace)
