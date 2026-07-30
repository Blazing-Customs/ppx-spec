"""Rewrite repo-root-relative links that arrive via `include-markdown`.

Several site pages are thin wrappers that pull in a canonical file from the
repository root (`SPEC.md`, `bindings/*.md`, `governance/*.md`). Those files
link to each other using paths that are correct when read on GitHub —
`governance/VERSIONING.md`, `bindings/mcp.md`, `SPEC.md#6-consent-model`.

`include-markdown` rewrites those to be relative to the *including* page, which
lands them outside `docs_dir` (e.g. `../../governance/VERSIONING.md` on the
`/spec/` page resolves to `blazing-customs.github.io/governance/...`). Every
such link 404s on the published site.

This hook catches any link that escapes `docs_dir`, re-reads the remainder as a
repo-root path, and points it at the equivalent site page — or, for files the
site does not render (raw schemas, examples), at the file on GitHub.
"""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

# Repo path -> path inside docs_dir. Directory keys have no trailing slash.
_TO_DOCS = {
    "SPEC.md": "spec.md",
    "CHANGELOG.md": "changelog.md",
    "README.md": "index.md",
    "governance": "governance/index.md",
    "governance/NAMESPACE-REGISTRATION.md": "governance/namespace-registration.md",
    "governance/VERSIONING.md": "governance/versioning.md",
    "governance/PROPOSAL-TEMPLATE.md": "governance/proposal-template.md",
    "governance/CONFORMANCE-LEVELS.md": "conformance.md",
    "bindings": "bindings/index.md",
    "bindings/mcp.md": "bindings/mcp.md",
    "bindings/a2a.md": "bindings/a2a.md",
    "bindings/ag-ui.md": "bindings/ag-ui.md",
    "bindings/a2ui.md": "bindings/a2ui.md",
    "bindings/http.md": "bindings/http.md",
    "schemas": "data-model/schemas.md",
    "examples": "data-model/examples.md",
}

# Repo paths with no site equivalent fall back to the source on GitHub.
_TO_SOURCE = ("schemas/", "examples/", "conformance", "registry/")

# Markdown inline links plus reference definitions.
_LINK = re.compile(r"(?<=]\()\s*(?P<target><[^>]+>|[^)\s]+)(?P<tail>[^)]*)\)")
_REFDEF = re.compile(r"(?m)^(?P<pre>\[[^\]]+]:\s*)(?P<target>\S+)")


def _repo_root(docs_dir: str) -> Path | None:
    """Walk up from docs_dir to the directory holding the canonical SPEC.md."""
    for parent in Path(docs_dir).resolve().parents:
        if (parent / "SPEC.md").is_file():
            return parent
    return None


def _blob_url(repo_url: str, repo_path: str) -> str:
    kind = "tree" if "." not in posixpath.basename(repo_path) else "blob"
    return f"{repo_url.rstrip('/')}/{kind}/main/{repo_path}"


def _rewrite_target(target: str, page_dir: str, escape_depth: int, repo_url: str):
    """Return the corrected target, or None to leave the link untouched."""
    if not target or "://" in target or target.startswith(("#", "/", "mailto:")):
        return None

    path, sep, fragment = target.partition("#")
    if not path:
        return None

    # Where does this link land, relative to docs_dir?
    landing = posixpath.normpath(posixpath.join(page_dir, path))
    if not landing.startswith(".."):
        return None  # stays inside the docs tree; mkdocs handles it

    # Strip exactly the `../` hops that leave docs_dir; the rest is a repo path.
    hops = 0
    remainder = landing
    while remainder.startswith("../"):
        hops += 1
        remainder = remainder[3:]
    if remainder == "..":
        hops += 1
        remainder = ""
    if hops != escape_depth:
        return None  # not a repo-root reference; leave it for mkdocs to warn on

    repo_path = remainder.rstrip("/")
    if repo_path in _TO_DOCS:
        docs_target = _TO_DOCS[repo_path]
        rebased = posixpath.relpath(docs_target, page_dir or ".")
        return rebased + sep + fragment

    if repo_path.startswith(_TO_SOURCE):
        return _blob_url(repo_url, repo_path) + sep + fragment

    return None


def on_page_markdown(markdown, page, config, files, **kwargs):
    root = _repo_root(config["docs_dir"])
    if root is None:
        return markdown
    # e.g. docs_dir=<repo>/site/docs -> a repo-root link escapes docs_dir twice.
    escape_depth = len(Path(config["docs_dir"]).resolve().relative_to(root).parts)
    repo_url = config.get("repo_url") or ""
    page_dir = posixpath.dirname(page.file.src_uri)

    def _inline(match):
        target = match.group("target")
        bare = target[1:-1] if target.startswith("<") else target
        new = _rewrite_target(bare, page_dir, escape_depth, repo_url)
        if new is None:
            return match.group(0)
        return f"{new}{match.group('tail')})"

    def _refdef(match):
        new = _rewrite_target(match.group("target"), page_dir, escape_depth, repo_url)
        if new is None:
            return match.group(0)
        return match.group("pre") + new

    markdown = _LINK.sub(_inline, markdown)
    return _REFDEF.sub(_refdef, markdown)
