"""trivy-scan command"""

from pathlib import Path

import click
from pydantic import BaseModel, Field

from cimd.classes.context import ApplicationContext
from cimd.classes.metadata import Item
from cimd.classes.shields_link import ShieldsLink


class Vulnerability(BaseModel):
    """Single vulnerability item"""

    id: str = Field(alias="VulnerabilityID")
    severity: str = Field(alias="Severity")


class TrivyScanResults(BaseModel):
    """Scan Results of a Trivy Scan"""

    target: str = Field(alias="Target")
    vulnerabilities: list[Vulnerability] = Field(alias="Vulnerabilities")


class TrivyScan(BaseModel):
    """Trivy Scan"""

    schema_version: int = Field(alias="SchemaVersion")
    results: list[TrivyScanResults] = Field(alias="Results")


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
    colors = {
        "CRITICAL": "red",
        "HIGH": "orange",
        "MEDIUM": "yellow",
        "LOW": "green",
        "UNKNOWN": "lightgray",
    }
    color = colors.get(severity, "blue")
    return ShieldsLink(label=severity, message=str(count), color=color, logo="trivy").to_string()


@click.command(name="trivy-scan")
@click.argument(
    "JSON_FILE",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True, resolve_path=True),
)
@click.option(
    "--replace",
    is_flag=True,
    show_default=True,
    help="Replace items in case they already exists.",
)
@click.pass_obj
def trivy_scan_command(app: ApplicationContext, json_file: str, replace: bool) -> None:
    """Extract metadata from a trivy scan JSON output file."""
    counter = count_json_file(json_file=json_file)
    for severity, count in counter.items():
        key = f"trivy-scan-{severity.lower()}"
        new_item = Item(
            value=str(count),
            label=severity,
            description=f"Count of found vulnerabilities with severity '{severity}'",
            image=image_for_severity_count(severity=severity, count=count),
        )
        app.add_item(key=key, item=new_item, replace=replace)
