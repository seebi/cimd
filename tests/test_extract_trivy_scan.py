"""Test extract trivy-scan command"""

import os
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from tests import FIXTURE_DIR, run


@dataclass
class FixtureData:
    """Test Data Fixture"""

    json_file: Path
    count: dict[str, str]


@pytest.fixture
def fixture_data(tmp_path: Path) -> Generator[FixtureData, Any, None]:
    """Provide TestSetup"""
    current_directory = Path.cwd()
    os.chdir(tmp_path)
    yield FixtureData(
        json_file=FIXTURE_DIR / "trivy-scan/debian:bullseye-20240926-slim.json",
        count={
            "trivy-scan-critical": "2",
            "trivy-scan-high": "10",
            "trivy-scan-low": "82",
            "trivy-scan-medium": "29",
            "trivy-scan-unknown": "1",
        },
    )
    # switch back to original directory
    os.chdir(current_directory)


def test_extract_trivy_scan(fixture_data: FixtureData) -> None:
    """Test extract trivy-scan command"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    assert run(command=("extract", "trivy-scan", str(_.json_file)))
    for key, value in _.count.items():
        assert run(command=("get", key)).lines[0] == value
