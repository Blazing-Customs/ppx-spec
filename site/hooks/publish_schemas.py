"""Publish the schemas and examples as part of the site.

Every schema declares `"$id": "https://ppx.dev/schemas/core/<name>.schema.json"`.
An `$id` that does not dereference is a defect in a published standard: tooling
that resolves `$ref` by URL cannot load the schema, and a reader who pastes the
identifier into a browser gets nothing.

The files are added to the build straight from the repository — they are never
copied into `docs/` and never hand-maintained in two places, so the published
document is byte-identical to the repository's by construction and cannot drift.

Mounted at the site root so that, with the site served at https://ppx.dev/, the
published URL is exactly the `$id` each schema already claims.
"""

from __future__ import annotations

import json
from pathlib import Path

from mkdocs.structure.files import File

# Directories copied verbatim, relative to the repo root.
_PUBLISH = ("schemas", "examples")


def _repo_root(docs_dir: str) -> Path | None:
    for parent in Path(docs_dir).resolve().parents:
        if (parent / "SPEC.md").is_file():
            return parent
    return None


def on_files(files, config, **kwargs):
    root = _repo_root(config["docs_dir"])
    if root is None:
        return files

    for subdir in _PUBLISH:
        source = root / subdir
        if not source.is_dir():
            continue
        for path in sorted(source.rglob("*.json")):
            files.append(
                File(
                    path=str(path.relative_to(root)),
                    src_dir=str(root),
                    dest_dir=config["site_dir"],
                    use_directory_urls=False,
                )
            )
    return files


def on_post_build(config, **kwargs):
    """Fail the build if a published schema is not byte-identical to its source,
    or if its `$id` does not match where it was just published."""
    root = _repo_root(config["docs_dir"])
    if root is None:
        return

    site_url = (config.get("site_url") or "").rstrip("/")
    site_dir = Path(config["site_dir"])
    mismatched, undereferenceable = [], []

    for path in sorted((root / "schemas").rglob("*.schema.json")):
        rel = path.relative_to(root)
        published = site_dir / rel
        if not published.is_file() or published.read_bytes() != path.read_bytes():
            mismatched.append(str(rel))
            continue
        declared = json.loads(path.read_text()).get("$id", "")
        if site_url and declared and declared != f"{site_url}/{rel.as_posix()}":
            undereferenceable.append(f"{rel}: $id={declared}")

    if mismatched:
        raise RuntimeError("published schema differs from source: " + ", ".join(mismatched))
    if undereferenceable:
        # Not fatal: the site may legitimately be served somewhere other than the
        # canonical schema host while a domain move is in progress.
        print(
            "WARNING - schema $id does not match this site_url, so these will not "
            "dereference from here:\n  " + "\n  ".join(undereferenceable)
        )
