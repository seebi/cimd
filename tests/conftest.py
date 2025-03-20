"""shared fixtures"""

from collections.abc import Generator
from os import chdir
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(autouse=True)
def new_dir(tmp_path: Path) -> Generator[Path, Any, None]:
    """Provide new test directory"""
    current_directory = Path.cwd()
    chdir(tmp_path)
    yield tmp_path
    # switch back to original directory
    chdir(current_directory)
