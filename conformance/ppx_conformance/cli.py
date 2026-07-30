"""`ppx-conformance` CLI. Runs the suite at one or more levels against a
specified provider URL and emits a PASS/FAIL verdict.

Usage:
    ppx-conformance --provider https://api.provider.app
    ppx-conformance --provider URL --level L2 --junit report.xml
    ppx-conformance --help
"""
from __future__ import annotations

import argparse
import sys

from ppx_conformance.runner import run


def _parse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ppx-conformance",
        description="Run the PPX conformance suite against a provider.",
    )
    p.add_argument(
        "--provider",
        required=True,
        help="Provider base URL (e.g. https://api.provider.app)",
    )
    p.add_argument(
        "--level",
        choices=["L1", "L2", "L3", "L4"],
        default="L1",
        help="Conformance level. Higher levels include all lower-level tests. Default: L1.",
    )
    p.add_argument(
        "--junit",
        default=None,
        help="Optional path for a JUnit XML report (for CI ingestion).",
    )
    p.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose pytest output."
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parse().parse_args(argv)
    summary = run(
        args.provider,
        level=args.level,
        junit=args.junit,
        verbose=args.verbose,
    )

    banner = "=" * 56
    print(banner)
    print(f"PPX conformance {args.level} :: {'PASS' if summary.passed else 'FAIL'}")
    print(f"Provider: {summary.provider_url}")
    if summary.junit_path:
        print(f"JUnit:    {summary.junit_path}")
    print(banner)
    return summary.exit_code


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
