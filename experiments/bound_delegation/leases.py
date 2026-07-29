"""Lease and per-action lifecycle checks."""

from __future__ import annotations

from .records import Lease


def lease_active(lease: Lease, step: int) -> bool:
    return lease.start_step <= step <= lease.end_step
