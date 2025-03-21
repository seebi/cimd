"""test extract coverage-xml command"""

from dataclasses import dataclass

import pytest

from cimd.commands.extract.coverage_xml import image_for_line_rate_item
from tests import FIXTURE_DIR, run, run_asserting_error


@dataclass
class FixtureData:
    """Test Data Fixture"""

    filepath = str(FIXTURE_DIR / "coverage-xml/coverage.xml")
    line_rate = "98.93"


@pytest.fixture
def fixture_data() -> FixtureData:
    """Provide TestSetup"""
    return FixtureData()


@pytest.mark.parametrize(
    ("line_rate", "color"),
    [
        (40, "red"),
        (50, "orange"),
        (70, "orange"),
        (75, "green"),
        (90, "brightgreen"),
        (95, "brightgreen"),
        (99, "brightgreen"),
    ],
)
def test_color(line_rate: float, color: str) -> None:
    """Test color selection"""
    assert image_for_line_rate_item(line_rate=line_rate).color == color


def test_success(fixture_data: FixtureData) -> None:
    """Test success"""
    assert run(command=("list", "--keys-only")).line_count == 0
    run(command=("extract", "coverage-xml", fixture_data.filepath))
    assert run(command=("list", "--keys-only")).line_count == 1
    assert run(command=("get", "coverage-xml-line-rate")).lines[0] == str(fixture_data.line_rate)


def test_fail() -> None:
    """Test fail"""
    assert run(command=("list", "--keys-only")).line_count == 0
    run_asserting_error(
        command=("extract", "coverage-xml", "__metadata__.json"), match="not well-formed"
    )
    run_asserting_error(command=("extract", "coverage-xml", "not-here.xml"), match="does not exist")
