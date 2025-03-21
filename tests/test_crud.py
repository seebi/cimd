"""CRUD tests"""

from collections.abc import Generator
from os import chdir
from pathlib import Path
from typing import Any

import pytest
from pydantic.dataclasses import dataclass

from tests import run, run_asserting_error


@dataclass
class FixtureData:
    """TestData"""

    key1: str = "coverage"
    value1: str = "80%"
    label1: str = "Code Coverage"
    description1: str = "pytest created test coverage percentage"
    comment1: str = "only a comment"
    image1: str = "https://github.com/seebi/cimd/actions/workflows/check.yml/badge.svg"
    link1: str = "https://github.com/seebi/cimd"


@pytest.fixture
def fixture_data() -> Generator[FixtureData, Any, None]:
    """Provide test data"""
    current_dir = Path(__file__).parent
    _ = FixtureData()
    yield _
    chdir(current_dir)


def test_basic_crud(fixture_data: FixtureData) -> None:
    """Test basic CRUD"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    run(command=("add", _.key1, _.value1))
    run_after_add = run(command=("list", "--keys-only"))
    assert run_after_add.line_count == 1
    assert _.key1 in run_after_add.stdout
    run_asserting_error(command=("add", _.key1, _.value1), match="already exists in file")
    run(command=("add", _.key1, _.value1, "--label", _.label1, "--replace"))
    assert run(command=("list", "--keys-only")).line_count == 1
    run_asserting_error(command=("delete", "unknown"), match="No items matching")
    run(command=("delete", _.key1))
    assert run(command=("list", "--keys-only")).line_count == 0
    run_asserting_error(command=("delete", _.key1), match="No items matching")
    run_asserting_error(command=("delete", "["), match="Invalid regular expression")


def test_optional_data_and_get(fixture_data: FixtureData) -> None:
    """Test optional data and get"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    run_asserting_error(command=("get", _.key1, "description"), match="does not exist")
    run(command=("add", _.key1, _.value1, "--label", _.label1, "--replace"))
    assert run(command=("get", _.key1)).lines[0] == _.value1
    assert run(command=("get", _.key1, "label")).lines[0] == _.label1
    run_asserting_error(command=("get", _.key1, "description"), match="has no attribute")

    run(command=("add", _.key1, _.value1, "--description", _.description1, "--replace"))
    assert run(command=("get", _.key1, "description")).lines[0] == _.description1
    run(command=("add", _.key1, _.value1, "--comment", _.comment1, "--replace"))
    assert run(command=("get", _.key1, "comment")).lines[0] == _.comment1
    run(command=("add", _.key1, _.value1, "--image", _.image1, "--replace"))
    assert run(command=("get", _.key1, "image")).lines[0] == _.image1
    run(command=("add", _.key1, _.value1, "--link", _.link1, "--replace"))
    assert run(command=("get", _.key1, "link")).lines[0] == _.link1


def test_table_list(fixture_data: FixtureData) -> None:
    """Test table list"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    run(
        command=(
            "add",
            _.key1,
            _.value1,
            "--label",
            _.label1,
            "--description",
            _.description1,
            "--comment",
            _.comment1,
            "--image",
            _.image1,
            "--link",
            _.link1,
        )
    )
    run_table = run(command=["list"])
    assert _.key1 in run_table.stdout
    assert _.value1 in run_table.stdout
    assert _.label1 in run_table.stdout
    assert _.description1 in run_table.stdout
    assert _.comment1 in run_table.stdout
    assert _.image1 in run_table.stdout
    assert _.link1 in run_table.stdout
