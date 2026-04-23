# Conformance Levels

A conforming PPX provider declares the highest level it supports. Each level
is cumulative: L2 implies L1, L3 implies L2, L4 implies L3.

## Level 1 — Portable Read

**Goal:** a user's profile can move out, and grant-scoped read access works
safely.

MUST implement:

- `/.well-known/ppx-card.json` discovery document.
- `GET  /v1/profile/summary`
- `POST /v1/profile/query`
- `GET  /v1/consent/grants`
- `POST /v1/consent/revoke`
- `POST /v1/export`
- OAuth 2.1 authorization on all authenticated endpoints.
- Deny-by-default on absent or invalid grants.
- Redaction to `allowed_claim_keys` / `allowed_namespaces`.
- Revocation takes effect within 60 seconds.
- Cross-domain denial when `cross_domain_transfer=deny`.

Conformance tests:

- `test_discovery_card.py`
- `test_deny_by_default.py`
- `test_redaction.py`
- `test_expired_grant.py`
- `test_revocation.py`
- `test_cross_domain_denial.py`

## Level 2 — Context-aware

Adds to L1:

- `POST /v1/profile/effective` with context-modifier resolution.
- Provenance and confidence surfaced on every returned claim.
- Context modifiers registered and applied per the extension descriptor.

## Level 3 — Interactive

Adds to L2:

- `POST /v1/profile/propose-updates` with `writeback_policy` enforcement.
- `POST /v1/profile/confirm-updates` for user/authorized confirmation.
- `GET  /v1/audit/events` for subject-visible access log.
- AG-UI event stream support for consent and review flows (see
  [`bindings/ag-ui.md`](../bindings/ag-ui.md)).
- Structured explanation support on returned claims.

Conformance tests (added):

- `test_writeback_pending.py`

## Level 4 — Multi-agent

Adds to L3:

- `POST /v1/derived-views/{kind}` — derived view construction (match,
  compatibility, recommendation_basis).
- Ephemeral grants (one-time-use with short TTL).
- MCP binding (see [`bindings/mcp.md`](../bindings/mcp.md)).
- A2A binding (see [`bindings/a2a.md`](../bindings/a2a.md)).
- Cross-namespace trait mapping for `allow_with_review` cross-domain flows.

## Declaring level

A provider's discovery card SHOULD include a `conformance_level` field
(L1–L4) indicating the highest level it claims. A provider MUST NOT claim a
level it has not validated against the current conformance suite.
