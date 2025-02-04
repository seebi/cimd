"""test_extract_pipeline_logs"""

import os
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

from tests import run, run_asserting_error


@dataclass
class FixtureData:
    """Test Data Fixture"""

    url: str
    pat: str
    project: str
    pipeline: str
    cmd: list[str]
    command: list[str]
    key_1: str = "hello"
    value_1: str = "🤓"
    key_2: str = "hi"
    value_2: str = "there"


@pytest.fixture
def fixture_data(tmp_path: Path) -> Generator[FixtureData, Any, None]:
    """Provide TestSetup"""
    current_directory = Path.cwd()
    os.chdir(tmp_path)
    if (url := os.environ.get("TEST_EXTRACT_PIPELINE_LOG_URL", "")) == "":
        pytest.skip("Need TEST_EXTRACT_PIPELINE_LOG_URL environment variable to run this test")
    if (pat := os.environ.get("TEST_EXTRACT_PIPELINE_LOG_PAT", "")) == "":
        pytest.skip("Need TEST_EXTRACT_PIPELINE_LOG_PAT environment variable to run this test")
    if (project := os.environ.get("TEST_EXTRACT_PIPELINE_LOG_PROJECT", "")) == "":
        pytest.skip("Need TEST_EXTRACT_PIPELINE_LOG_PROJECT environment variable to run this test")
    if (pipeline := os.environ.get("TEST_EXTRACT_PIPELINE_LOG_PIPELINE", "")) == "":
        pytest.skip("Need TEST_EXTRACT_PIPELINE_LOG_PIPELINE environment variable to run this test")
    yield FixtureData(
        url=url,
        pat=pat,
        project=project,
        pipeline=pipeline,
        command=["extract", "pipeline-logs", "--url", url, "--pat", pat, "--project", project],
        cmd=["extract", "pipeline-logs"],
    )
    # switch back to original directory
    os.chdir(current_directory)


def test_extract(fixture_data: FixtureData) -> None:
    """Test extract pipeline-logs command"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    pipeline_command = _.command.copy()
    pipeline_command.extend(["--pipeline", _.pipeline])
    run(command=pipeline_command)
    assert run(command=("list", "--keys-only")).line_count == 1 + 1
    assert run(command=("get", _.key_1)).lines[0] == _.value_1
    assert run(command=("get", _.key_2)).lines[0] == _.value_2


def test_extract_fail(fixture_data: FixtureData) -> None:
    """Test failing pipeline-logs command"""
    _ = fixture_data
    assert run(command=("list", "--keys-only")).line_count == 0
    pipeline_command = _.command.copy()
    pipeline_command.extend(["--pipeline", "123123123123"])
    run_asserting_error(command=pipeline_command, match="404 Not found (Gitlab Error)")
    assert run(command=("list", "--keys-only")).line_count == 0
    command = _.cmd.copy()
    command.extend(["--pat", _.pat])
    run_asserting_error(
        command=command,
        match="Either use the --project option or set the CI_PROJECT_ID",
    )
    command.extend(["--project", _.project])
    run_asserting_error(
        command=command,
        match="Either use the --pipeline option or set the CI_PIPELINE_ID",
    )
