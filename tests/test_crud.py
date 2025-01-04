"""CRUD tests"""

from collections.abc import Generator
from os import chdir
from pathlib import Path
from typing import Any

import pytest
from pydantic.dataclasses import dataclass

from tests import run, run_asserting_error


@dataclass
class TestData:
    """TestData"""

    key1: str = "coverage"
    value1: str = "80%"
    label1: str = "Code Coverage"


@pytest.fixture
def test_data() -> Generator[TestData, Any, None]:
    """Provide test data"""
    current_dir = Path(__file__).parent
    _ = TestData()
    yield _
    chdir(current_dir)


def test_basic_crud(tmp_path: Path, test_data: TestData) -> None:
    """Test basic CRUD"""
    chdir(tmp_path)
    _ = test_data
    assert run(command=("list", "--keys-only")).line_count == 0
    run(command=("add", _.key1, _.value1))
    run_after_add = run(command=("list", "--keys-only"))
    assert run_after_add.line_count == 1
    assert _.key1 in run_after_add.stdout
    run_asserting_error(command=("add", _.key1, _.value1), match="already exists in file")
    run(command=("add", _.key1, _.value1, "--label", _.label1, "--replace"))
    assert run(command=("list", "--keys-only")).line_count == 1
    run(command=("delete", _.key1))
    assert run(command=("list", "--keys-only")).line_count == 0
    run_asserting_error(command=("delete", _.key1), match="does not exist in file")
