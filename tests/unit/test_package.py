from __future__ import annotations

import importlib
import importlib.metadata
import tomllib
from pathlib import Path

import pytest

import arx_mentis

ROOT = Path(__file__).parents[2]


def test_version_matches_installed_distribution() -> None:
    assert arx_mentis.__version__ == importlib.metadata.version("arx_mentis")


def test_project_metadata_and_runtime_dependencies() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
        "project"
    ]
    assert project["name"] == "arx_mentis"
    assert project["requires-python"] == ">=3.13"
    assert project["dependencies"] == []
    assert project["version"] == arx_mentis.__version__


@pytest.mark.parametrize(
    "module_name",
    [
        "arx_mentis.frontend",
        "arx_mentis.syntax",
        "arx_mentis.semantics",
        "arx_mentis.runtime",
        "arx_mentis.diagnostics",
        "arx_mentis.adapters",
        "arx_mentis.backends",
        "arx_mentis.backends.python_reference",
        "arx_mentis.ir",
    ],
)
def test_stage_zero_boundaries_import(module_name: str) -> None:
    assert importlib.import_module(module_name).__name__ == module_name


def test_stage_zero_has_no_runtime_values_module() -> None:
    assert importlib.util.find_spec("arx_mentis.runtime.values") is None
