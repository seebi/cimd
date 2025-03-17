"""Test extract trivy-scan command"""

import os
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from tests import FIXTURE_DIR, run

COUNTS = {
    "debian:bullseye-20240926-slim.json": {
        "trivy-scan-critical": "2",
        "trivy-scan-high": "10",
        "trivy-scan-low": "82",
        "trivy-scan-medium": "29",
        "trivy-scan-unknown": "1",
    },
    "seebi:cimd.json": {
        "trivy-scan-high": "3",
    },
}


@dataclass
class FixtureData:
    """Test Data Fixture"""

    counts: dict[str, dict[str, str]]


@pytest.fixture
def fixture_data(tmp_path: Path) -> Generator[FixtureData, Any, None]:
    """Provide TestSetup"""
    current_directory = Path.cwd()
    os.chdir(tmp_path)
    yield FixtureData(
        counts=COUNTS,
    )
    # switch back to original directory
    os.chdir(current_directory)


@pytest.mark.parametrize("filename", COUNTS.keys())
def test_extract_trivy_scans(fixture_data: FixtureData, filename: str) -> None:
    """Test extract trivy-scan command with file 1"""
    filepath = str(FIXTURE_DIR / f"trivy-scan/{filename}")
    counts = fixture_data.counts[filename]
    assert run(command=("list", "--keys-only")).line_count == 0
    assert run(command=("extract", "trivy-scan", filepath))
    for key, value in counts.items():
        assert run(command=("get", key)).lines[0] == value


@pytest.mark.parametrize("filename", ["seebi:cimd.json"])
def test_extract_all_option(fixture_data: FixtureData, filename: str) -> None:
    """Test --all option"""
    filepath = str(FIXTURE_DIR / f"trivy-scan/{filename}")
    counts = fixture_data.counts[filename]
    assert run(command=("list", "--keys-only")).line_count == 0
    assert run(command=("extract", "trivy-scan", filepath, "--all", "--replace"))
    all_keys = run(command=("list", "--keys-only")).line_count
    assert all_keys > len(counts.keys())


@pytest.mark.parametrize("filename", ["seebi:cimd.json"])
def test_extract_severity_option(fixture_data: FixtureData, filename: str) -> None:
    """Test --severity option"""
    filepath = str(FIXTURE_DIR / f"trivy-scan/{filename}")
    counts = fixture_data.counts[filename]
    assert run(command=("list", "--keys-only")).line_count == 0
    assert run(command=("extract", "trivy-scan", filepath, "--severity", "CRITICAL"))
    assert run(command=("list", "--keys-only")).line_count == 1
    assert run(command=("extract", "trivy-scan", filepath, "--severity", "HIGH"))
    assert run(command=("list", "--keys-only")).line_count == 1 + 1
    assert run(command=("get", "trivy-scan-critical")).lines[0] == counts.get(
        "trivy-scan-critical", "0"
    )
    assert run(command=("get", "trivy-scan-high")).lines[0] == counts.get("trivy-scan-high", "0")
