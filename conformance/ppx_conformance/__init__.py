"""PPX conformance test harness.

Public surface:
    ppx_conformance.run(provider_url, level="L1", junit=None) -> ReportSummary
    ppx_conformance.cli()  — CLI entry point (`ppx-conformance ...`)
"""

from ppx_conformance.runner import ReportSummary, run
from ppx_conformance.cli import main as cli

__version__ = "0.1.0"
__all__ = ["run", "ReportSummary", "cli", "__version__"]
