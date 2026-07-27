from __future__ import annotations

import platform
import sys

import pytest

import arx_mentis
from arx_mentis.cli import main


def test_version_output_is_derived_from_package(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == f"Arx_Mentis {arx_mentis.__version__}"


def test_doctor_reports_required_fields(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["doctor"]) == 0
    output = capsys.readouterr().out
    assert "import: ok" in output
    assert "package: arx_mentis" in output
    assert f"version: {arx_mentis.__version__}" in output
    assert f"python implementation: {platform.python_implementation()}" in output
    assert f"python version: {platform.python_version()}" in output
    assert f"executable: {sys.executable}" in output
    assert "platform:" in output


def test_status_names_stage_and_unimplemented_layers(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(["status"]) == 0
    output = capsys.readouterr().out
    assert "Stage 0" in output
    for layer in ("syntax", "semantics", "runtime", "IR"):
        assert f"{layer}: unimplemented" in output


@pytest.mark.parametrize("arguments", [[], ["unknown"], ["version", "extra"]])
def test_argparse_usage_failures_exit_two(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2
