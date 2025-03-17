"""trivy-scan command"""

from pathlib import Path

import click
from pydantic import BaseModel, Field

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item
from cimd.classes.shields_link import ShieldsLink

COLORS = {
    "CRITICAL": "red",
    "HIGH": "orange",
    "MEDIUM": "yellow",
    "LOW": "green",
    "UNKNOWN": "lightgray",
}


class Vulnerability(BaseModel):
    """Single vulnerability item"""

    id: str = Field(alias="VulnerabilityID")
    severity: str = Field(alias="Severity")


class TrivyScanResults(BaseModel):
    """Scan Results of a Trivy Scan"""

    target: str = Field(alias="Target")
    vulnerabilities: list[Vulnerability] = Field(alias="Vulnerabilities", default_factory=list)


class TrivyScan(BaseModel):
    """Trivy Scan"""

    schema_version: int = Field(alias="SchemaVersion")
    results: list[TrivyScanResults] = Field(alias="Results", default_factory=list)


def count_json_file(json_file: str) -> dict[str, int]:
    """Count a json file"""
    scan = TrivyScan.model_validate_json(Path(json_file).read_text())
    counter: dict[str, int] = {}
    for result in scan.results:
        for vulnerability in result.vulnerabilities:
            counter[vulnerability.severity] = counter.get(vulnerability.severity, 0) + 1
    return counter


def image_for_severity_count(severity: str, count: int) -> str:
    """Create a shields.io image for a severity count"""
    severity = severity.upper()
    color = COLORS.get(severity, "blue")
    return ShieldsLink(label=severity, message=str(count), color=color, logo="trivy").to_string()


@click.command(name="trivy-scan")
@click.argument(
    "JSON_FILE",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--severity",
    type=click.Choice(list(COLORS.keys()), case_sensitive=False),
    help="Request a single severity group only. This results in explicit zero counts.",
)
@click.option(
    "--all",
    "all_",
    is_flag=True,
    help="Will explicitly extract all known severity groups, even zero counts.",
)
@click.option(
    "--replace",
    is_flag=True,
    help="Replace items in case they already exists.",
)
@click.pass_obj
def trivy_scan_command(
    app: ApplicationContext, json_file: str, severity: str, all_: bool, replace: bool
) -> None:
    """Extract metadata from a trivy scan JSON output file.

    This command will extract counts of vulnerabilities, grouped by
    severity. Per default, only severity groups with at least one
    vulnerability will be extracted. If you need explicit zero counts,
    use `--severity` or `--all`.
    """
    counter = count_json_file(json_file=json_file)
    severities = [severity] if severity else counter.keys()
    if all_:
        severities = list(COLORS.keys())
        severities.extend(counter.keys())
        severities = list(set(severities))
    for _ in severities:
        count = counter.get(_, 0)
        key = f"trivy-scan-{_.lower()}"
        new_item = Item(
            value=str(count),
            label=_,
            description=f"Count of found vulnerabilities with severity '{_}'",
            image=image_for_severity_count(severity=_, count=count),
        )
        app.add_item(key=key, item=new_item, replace=replace)
