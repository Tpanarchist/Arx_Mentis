from __future__ import annotations

import importlib.metadata
import os
import subprocess
import sys
from pathlib import Path

import pytest

import arx_mentis


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        check=False,
        capture_output=True,
        text=True,
    )


def test_module_invocation() -> None:
    result = run(sys.executable, "-m", "arx_mentis", "version")
    assert result.returncode == 0
    assert result.stdout.strip() == f"Arx_Mentis {arx_mentis.__version__}"
    assert result.stderr == ""


def test_console_entry_point_metadata() -> None:
    matches = [
        entry_point
        for entry_point in importlib.metadata.entry_points(group="console_scripts")
        if entry_point.name == "arx-mentis"
    ]
    assert len(matches) == 1
    assert matches[0].value == "arx_mentis.cli:main"


def test_installed_console_command() -> None:
    script_name = "arx-mentis.exe" if os.name == "nt" else "arx-mentis"
    executable = Path(sys.executable).with_name(script_name)
    assert executable.is_file()
    result = run(str(executable), "version")
    assert result.returncode == 0
    assert result.stdout.strip() == f"Arx_Mentis {arx_mentis.__version__}"
    assert result.stderr == ""


@pytest.mark.parametrize("arguments", [(), ("unknown",), ("doctor", "extra")])
def test_module_usage_failures_exit_two(arguments: tuple[str, ...]) -> None:
    result = run(sys.executable, "-m", "arx_mentis", *arguments)
    assert result.returncode == 2
    assert "usage: arx-mentis" in result.stderr
