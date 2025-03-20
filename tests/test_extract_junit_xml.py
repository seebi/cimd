"""test extract junit-xml command"""

from dataclasses import dataclass

import pytest

from tests import FIXTURE_DIR, run, run_asserting_error


@dataclass
class FixtureData:
    """Test Data Fixture"""

    filepath = str(FIXTURE_DIR / "junit/junit-pytest.xml")
    counts: dict[str, int]


@pytest.fixture
def fixture_data() -> FixtureData:
    """Provide TestSetup"""
    return FixtureData(
        counts={
            "junit-xml-errors": 3,
            "junit-xml-failures": 2,
            "junit-xml-skipped": 2,
            "junit-xml-succeeded": 7,
        }
    )


def test_success(fixture_data: FixtureData) -> None:
    """Test success"""
    assert run(command=("list", "--keys-only")).line_count == 0
    run(command=("extract", "junit-xml", fixture_data.filepath))
    assert run(command=("list", "--keys-only")).line_count > 0
    for key, value in fixture_data.counts.items():
        assert run(command=("get", key)).lines[0] == str(value)


def test_fail() -> None:
    """Test fail"""
    assert run(command=("list", "--keys-only")).line_count == 0
    run_asserting_error(
        command=("extract", "junit-xml", "__metadata__.json"), match="not well-formed"
    )
    run_asserting_error(command=("extract", "junit-xml", "not-here.xml"), match="does not exist")
