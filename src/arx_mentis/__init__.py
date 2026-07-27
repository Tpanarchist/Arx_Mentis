"""Top-level package metadata for Arx Mentis."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("arx_mentis")
except PackageNotFoundError:
    # Source-tree fallback: keep this bootstrap value aligned with pyproject.toml.
    __version__ = "0.1.0"

__all__ = ["__version__"]
