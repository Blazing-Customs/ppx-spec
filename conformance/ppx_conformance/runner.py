"""Programmatic runner — thin wrapper over pytest so this suite is usable
from CI, from a Python script, or from the CLI, with the same results.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import pytest


_LEVELS = {"L1", "L2", "L3", "L4"}


@dataclass
class ReportSummary:
    level: str
    provider_url: str
    exit_code: int
    # pytest's ExitCode enum: 0 OK, 1 tests failed, 2 collection, etc.
    junit_path: str | None = None
    # Not trying to parse JUnit ourselves; caller can read the XML if they want.
    extras: dict[str, str] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.exit_code == 0


def run(
    provider_url: str,
    *,
    level: str = "L1",
    junit: str | None = None,
    verbose: bool = False,
    extra_args: list[str] | None = None,
) -> ReportSummary:
    """Run the conformance suite at the given level against a provider URL.

    Args:
        provider_url: Base URL of the provider. Must be reachable.
        level: One of "L1" (default), "L2", "L3", "L4". Higher levels imply
            all lower levels will also run.
        junit: Optional path to write a JUnit XML report (for CI ingestion).
        verbose: Pass `-v` to pytest.
        extra_args: Any additional pytest flags.

    Returns:
        ReportSummary with `.passed`, `.exit_code`, and the junit path used.
    """
    level = level.upper()
    if level not in _LEVELS:
        raise ValueError(f"level must be one of {sorted(_LEVELS)}; got {level!r}")

    env_key = "PPX_PROVIDER_URL"
    os.environ[env_key] = provider_url

    tests_dir = Path(__file__).resolve().parent.parent / "tests"
    if not tests_dir.exists():
        raise RuntimeError(f"conformance tests directory not found at {tests_dir}")

    # Pytest marker selector — level1 is always included. Running L3 means
    # "all of level1 + level2 + level3" tests execute.
    target_levels = sorted(level_to_markers(level))
    marker_expr = " or ".join(target_levels)

    argv: list[str] = [str(tests_dir), "-m", marker_expr, "--strict-markers", "-ra"]
    if verbose:
        argv.append("-v")
    if junit:
        argv += ["--junitxml", junit]
    if extra_args:
        argv += extra_args

    code = pytest.main(argv)
    return ReportSummary(
        level=level,
        provider_url=provider_url,
        exit_code=int(code),
        junit_path=junit,
    )


def level_to_markers(level: str) -> set[str]:
    """L3 implies L1+L2+L3; L1 is always included (includes schema-only tests)."""
    idx = int(level[1])
    out = {"schema"}
    for i in range(1, idx + 1):
        out.add(f"level{i}")
    return out
