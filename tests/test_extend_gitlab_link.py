"""Test extend gitlab-link command"""

from collections.abc import Generator
from os import chdir
from pathlib import Path
from typing import Any

import pytest

from tests import run, run_asserting_error


@pytest.fixture
def new_dir(tmp_path: Path) -> Generator[Path, Any, None]:
    """Provide new test directory"""
    current_directory = Path.cwd()
    chdir(tmp_path)
    yield tmp_path
    # switch back to original directory
    chdir(current_directory)


def test_fails() -> None:
    """Test failing commands"""
    extend_cmd = ["extend", "gitlab-link", "--artifact-path", "dir/file", "--key", "ttt"]
    run_asserting_error(
        command=extend_cmd,
        match="Either use the --job option or set the CI_JOB_URL environment variable.",
    )


@pytest.mark.usefixtures("new_dir")
def test_success() -> None:
    """Test update links - successful commands"""
    extend_cmd = [
        "extend",
        "gitlab-link",
        "--job-url",
        "https:/example.org/",
        "--artifact-path",
        "dir/file",
        "--key",
    ]
    url = "https:/example.org/artifacts/raw/dir/file"
    items = [("key", "value"), ("key2", "value2"), ("key3", "value3")]
    assert run(command=("list", "--keys-only")).line_count == 0
    for key, value in items:
        assert run(command=("add", key, value))
    assert run(command=("list", "--keys-only")).line_count == len(items)
    for key, _value in items:
        assert run_asserting_error(command=("get", key, "link"), match="has no attribute")
        run(command=(*extend_cmd, key))
        assert run(command=("get", key, "link")).lines[0] == url

    run(command=("delete", ".*"))
    assert run(command=("list", "--keys-only")).line_count == 0
    for key, value in items:
        assert run(command=("add", key, value))
    run(command=(*extend_cmd, "key.+"))
    assert run_asserting_error(command=("get", "key", "link"), match="has no attribute")
    assert run(command=("get", "key2", "link")).lines[0] == url
    assert run(command=("get", "key3", "link")).lines[0] == url
