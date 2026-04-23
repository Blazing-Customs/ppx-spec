# Consent Grant

A **Consent Grant** is a first-class, user-controlled authorization. It
defines who may access which claims, for what purpose, under what
constraints, for how long.

## Shape

```json
{%
  include "../../../examples/grant-fragrance.json"
%}
```

## Scope axes

A grant scopes on six axes:

1. `purposes` — e.g. `recommendation`, `ranking`, `matching`, `explanation`.
2. `allowed_domains` — e.g. `fragrance`, `travel`.
3. `allowed_namespaces` — e.g. `core`, `fragrance`.
4. `allowed_claim_keys` — explicit keys (optional; if present, narrows).
5. `allowed_operations` — `read`, `query`, `propose_update`, etc.
6. `expires_at` — every grant has time-bounded authority.

## Policies

- `cross_domain_transfer` — `deny` (default), `allow_with_review`,
  `allow_if_same_provider`, `allow`.
- `writeback_policy` — `forbidden`, `review_required` (default),
  `auto_for_low_risk`, `allow`.
- `redisclosure` — `forbidden` (default), `same_purpose_only`, `allow`.

## Lifecycle

`status` is one of `active`, `expired`, `revoked`, `pending`.

Revocation takes effect within 60 seconds ([§10 Security & privacy](../spec.md#10-security-and-privacy-requirements)).

## Audit

Grants may opt into per-access logging and writeback notifications:

```json
"audit": {
  "log_access": true,
  "notify_on_writeback": true
}
```

## See also

- [Consent & trust](../consent-and-trust.md)
- [Schema: consent-grant.schema.json](https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/consent-grant.schema.json)
