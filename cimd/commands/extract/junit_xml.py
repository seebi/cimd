"""junit-xml command"""

from xml.etree.ElementTree import ParseError

import click
from junitparser import JUnitXml

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item
from cimd.classes.shields_link import ShieldsLink

COLORS = {
    "FAILURES": "red",
    "ERRORS": "orange",
    "SKIPPED": "yellow",
    "SUCCEEDED": "green",
}


def image_for_junit_key(key: str, count: int) -> str:
    """Create a shields.io image for a junit key"""
    key = key.upper()
    color = COLORS.get(key, "blue")
    return ShieldsLink(label=f"Tests {key.title()}", message=f"{count!s}", color=color).to_string()


@click.command(name="junit-xml")
@click.argument(
    "XML_FILE",
    nargs=-1,
    type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace items in case they already exists.",
)
@click.pass_obj
def junit_xml_command(app: ApplicationContext, xml_file: str, replace: bool) -> None:
    """Extract metadata from a JUnit XML output files.

    This command will extract counts of test cases, grouped by
    status (errors, failures, skipped, succeeded). Multiple input files
    will result in an overall count.
    """
    xml = JUnitXml()
    for file in xml_file:
        try:
            xml += JUnitXml.fromfile(file)
            app.echo_debug(f"{file} parsed: {xml.tests} overall tests")
        except ParseError as error:
            raise click.UsageError(f"{file} - {error!s}") from error
    counter: dict[str, int] = {
        "errors": xml.errors,
        "failures": xml.failures,
        "skipped": xml.skipped,
        "succeeded": xml.tests - xml.errors - xml.failures - xml.skipped,
    }
    for _ in counter:
        count = counter.get(_, 0)
        key = f"junit-xml-{_.lower()}"
        new_item = Item(
            value=str(count),
            label=f"Tests {_.title()}",
            description=f"JUnit count of {_} tests ({xml_file})",
            image=image_for_junit_key(key=_, count=count),
        )
        app.add_item(key=key, item=new_item, replace=replace)
