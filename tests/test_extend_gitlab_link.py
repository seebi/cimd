"""Test extend gitlab-link command"""

from _pytest.monkeypatch import MonkeyPatch

from tests import run, run_asserting_error


def test_fails() -> None:
    """Test failing commands"""
    extend_cmd = ["extend", "gitlab-link", "--artifact-path", "dir/file", "ttt"]
    run_asserting_error(
        command=extend_cmd,
        match="Either use the --job option or set the CI_JOB_URL environment variable.",
    )


def test_with_env(monkeypatch: MonkeyPatch) -> None:
    """Test extend gitlab-link command with environment variables"""
    extend_cmd = ["extend", "gitlab-link", "--artifact-path", "dir/file", "key"]
    assert run(command=("list", "--keys-only")).line_count == 0
    assert run(command=("add", "key", "value"))
    assert run(command=("list", "--keys-only")).line_count == 1
    run_asserting_error(
        command=["get", "key", "link"],
        match="has no attribute",
    )
    run_asserting_error(
        command=extend_cmd,
        match="Either use the --job option or set the CI_JOB_URL environment variable.",
    )
    monkeypatch.setenv("CI_JOB_URL", "https://example.org/")
    run(command=extend_cmd)
    run(["get", "key", "link"])


def test_url_generation() -> None:
    """Test update links - url generation"""
    extend_cmd = [
        "extend",
        "gitlab-link",
        "--artifact-path",
        "dir/file",
        "key",
        "--job-url",
    ]
    host_prot = "https://example.org"
    url = f"{host_prot}/artifacts/raw/dir/file"
    run(command=("add", "key", "value"))
    assert run(command=("list", "--keys-only")).line_count == 1
    run(command=(*extend_cmd, host_prot))
    assert run(command=("get", "key", "link")).lines[0] == url
    run(command=(*extend_cmd, host_prot + "/"))
    assert run(command=("get", "key", "link")).lines[0] == url


def test_success() -> None:
    """Test update links - successful commands"""
    extend_cmd = [
        "extend",
        "gitlab-link",
        "--job-url",
        "https:/example.org/",
        "--artifact-path",
        "dir/file",
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
