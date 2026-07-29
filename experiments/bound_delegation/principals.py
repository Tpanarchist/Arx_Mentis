"""Named neutral principals."""

from __future__ import annotations

from .records import Principal


def standard_principal() -> Principal:
    return Principal("principal-p", "grant:p", resource_access=3)
