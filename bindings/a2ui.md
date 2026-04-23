# Binding: PPX over A2UI

**Target:** A2UI **v0.8** (stable). v0.9 is draft and is NOT cited
normatively in v0.1 of PPX.

This document is normative for providers claiming the `a2ui_supported` UI
capability in their discovery card.

## Overview

A2UI provides a transport-agnostic, declarative UI layer. PPX defines a small
set of recommended A2UI component archetypes so that any A2UI-capable client
can render profile cards, grant cards, diff views, and consent prompts
consistently across providers.

A2UI v0.8 uses a **flat adjacency-list** structure: components reference
child IDs rather than nesting. PPX-recommended archetypes below are defined
at that shape.

## Component archetypes

### `ClaimCard`

Displays a single claim with provenance, confidence, and review state.

```json
{
  "id": "claim-card-1",
  "type": "Card",
  "children": ["claim-title-1", "claim-value-1", "claim-source-1", "claim-actions-1"],
  "data": {
    "claim": { "$ref": "#/data/claim" }
  }
}
```

Required sub-components:

- a title bound to `claim.key` (prettified)
- a value widget appropriate to `value_type` (slider for float, chip list
  for map<string,float>, badge for string)
- a provenance/confidence line bound to `claim.source.kind` and
  `claim.confidence`, rendered distinctly for `user_stated` vs inferred
- action buttons bound to `confirm`, `edit`, `reject`

### `GrantCard`

Displays a consent grant with its scope, expiry, and revoke action.

```json
{
  "id": "grant-card-1",
  "type": "Card",
  "children": ["grant-grantee-1", "grant-scope-1", "grant-expiry-1", "grant-actions-1"],
  "data": {
    "grant": { "$ref": "#/data/grant" }
  }
}
```

Required sub-components:

- grantee identity
- scope summary (domains, namespaces, allowed_claim_keys count)
- expiry with relative time (e.g. "expires in 23 days")
- revoke action

### `ProfileDiffView`

Displays a claim-level diff over time.

```json
{
  "id": "profile-diff-1",
  "type": "List",
  "children": ["diff-row-1", "diff-row-2"],
  "data": {
    "diff": { "$ref": "#/data/diff" }
  }
}
```

### `ConsentRequestForm`

Surfaced by the AG-UI `INTERRUPT` event (see [`ag-ui.md`](ag-ui.md)).

Fields (all editable before approval):

- requested purposes (multi-select)
- allowed domains
- allowed namespaces
- allowed_claim_keys (pre-populated by grantee request, user can narrow)
- expiry (date/time; user can shorten)
- cross_domain_transfer (toggle set; default `deny`)
- writeback_policy (toggle set; default `review_required`)

## Data binding

All PPX A2UI components use JSON Pointer (RFC 6901) data bindings per A2UI
v0.8. The data model MUST be the raw PPX object (Claim, ConsentGrant, etc.),
unmodified — the binding layer does not transform data.

## Message types

PPX surfaces rendered via A2UI use the standard A2UI message lifecycle:
`createSurface`, `updateComponents`, `updateDataModel`, `deleteSurface`.

## Non-goals

- This binding does not define the visual design of components.
- This binding does not define interactions beyond what A2UI v0.8 supports.
