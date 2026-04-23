# Versioning Policy

PPX uses **two** distinct versioning tracks:

## 1. Normative spec document

Tracked as `MAJOR.MINOR.PATCH-STAGE` with a dated release. Examples:

- `0.1.0-draft` (first draft)
- `0.2.0-draft`
- `1.0.0` (first stable)
- `1.1.0-rc1`

Rules:

- **Pre-1.0**: any release MAY introduce breaking changes; the `-draft`
  suffix MUST be present until a release passes the stabilization criteria.
- **1.0+**: MAJOR bump = backward-incompatible change to normative semantics;
  MINOR bump = backward-compatible additions; PATCH = clarifications only, no
  semantic change.

## 2. Schemas

Each JSON Schema under `schemas/` is versioned by its `$id`:

```
https://ppx.dev/schemas/core/profile.schema.json
```

The **content** of a schema evolves in lockstep with the normative spec
version. Providers wanting to pin to a specific schema MUST reference it via
a tagged release URL:

```
https://raw.githubusercontent.com/Blazing-Customs/ppx-spec/v0.1.0-draft/schemas/core/profile.schema.json
```

## Deprecation

1. A field or key is first marked deprecated in a release's changelog.
2. It remains accepted for at least one subsequent MINOR release.
3. It is removed no earlier than the next MAJOR release.

## Stabilization criteria for 1.0

- All v0.1 "open questions" (see [`SPEC.md §15`](../SPEC.md#15-open-questions-for-v02))
  are either resolved or explicitly deferred.
- At least two interoperable implementations of every conformance level
  claimed `stable`.
- Public comment period of at least 60 days with no unresolved blocking
  issues.
- Approval by the Editors (see `governance/` root or equivalent).

## Adjacent-standard version pinning

Binding documents pin the adjacent-standard version they target (e.g. MCP
`2025-11-25`, A2A v1.2, AG-UI 0.1.0, A2UI v0.8). Upgrading a binding's target
version is a MINOR bump to the PPX spec if backward-compatible, otherwise
MAJOR.
