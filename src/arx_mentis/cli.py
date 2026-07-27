"""Stage 0 command-line interface for Arx Mentis."""

from __future__ import annotations

import argparse
import platform
import sys
from collections.abc import Sequence

from arx_mentis import __version__


def _version(_args: argparse.Namespace) -> int:
    print(f"Arx_Mentis {__version__}")
    return 0


def _doctor(_args: argparse.Namespace) -> int:
    print("Arx Mentis doctor")
    print("import: ok")
    print("package: arx_mentis")
    print(f"version: {__version__}")
    print(f"python implementation: {platform.python_implementation()}")
    print(f"python version: {platform.python_version()}")
    print(f"executable: {sys.executable}")
    print(f"platform: {platform.platform()}")
    return 0


def _status(_args: argparse.Namespace) -> int:
    print("Arx Mentis Stage 0")
    print("syntax: unimplemented")
    print("semantics: unimplemented")
    print("runtime: unimplemented")
    print("IR: unimplemented")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the Stage 0 argument parser without performing any I/O."""
    parser = argparse.ArgumentParser(prog="arx-mentis")
    subparsers = parser.add_subparsers(dest="command", required=True)

    version_parser = subparsers.add_parser("version", help="show package version")
    version_parser.set_defaults(handler=_version)

    doctor_parser = subparsers.add_parser(
        "doctor", help="report installation and interpreter details"
    )
    doctor_parser.set_defaults(handler=_doctor)

    status_parser = subparsers.add_parser("status", help="show implementation stage")
    status_parser.set_defaults(handler=_status)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface and return a process status."""
    args = build_parser().parse_args(argv)
    return args.handler(args)
