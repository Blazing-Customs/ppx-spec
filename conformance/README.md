# PPX Conformance Suite

Executable tests that a PPX provider (or a schema-only target) must pass to
claim conformance at each level.

## Install

```bash
cd conformance
pip install -e .
```

## Run

Schema-only tests (no provider required):

```bash
pytest -m schema
```

All tests against a running provider:

```bash
PPX_PROVIDER_URL=https://your-provider.example.com \
PPX_PROVIDER_TOKEN=<oauth-access-token> \
pytest
```

Run a specific conformance level:

```bash
pytest -m level1
pytest -m level2
```

## Test inventory

| File | Level | What it checks |
|---|---|---|
| `test_schema_roundtrip.py` | schema | Every example in `examples/` validates against its schema. |
| `test_discovery_card.py` | L1 | Provider serves a valid `/.well-known/ppx-card.json`. |
| `test_deny_by_default.py` | L1 | Any access without an active grant is denied. |
| `test_redaction.py` | L1 | Responses never include fields outside a grant's `allowed_claim_keys` / `allowed_namespaces`. |
| `test_expired_grant.py` | L1 | An access token whose grant is past `expires_at` is rejected. |
| `test_revocation.py` | L1 | Access via a revoked grant fails within 60 seconds of revocation. |
| `test_writeback_pending.py` | L3 | `propose_updates` with `writeback_policy=review_required` creates a pending review, never a direct write. |
| `test_cross_domain_denial.py` | L1 | A grant with `cross_domain_transfer=deny` rejects requests that cross domain. |
