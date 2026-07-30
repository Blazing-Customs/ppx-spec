# Binding: PPX over HTTP

**Target:** plain HTTP/JSON REST.

This document is normative for providers claiming the `http_api` transport
binding in their discovery card.

## Base conventions

- All request and response bodies are JSON (`application/json`).
- All authenticated requests use `Authorization: Bearer <token>` per OAuth 2.1.
- All timestamps are RFC 3339 (`date-time`) in UTC.
- All IDs follow the `ppx:<type>:<id>` URN-style format.

## Endpoint catalog

### Discovery

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/.well-known/ppx-card.json` | none | Provider discovery card. |

### OAuth

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/oauth/authorize` | user session | Authorization endpoint. |
| `POST` | `/oauth/token` | client creds / PKCE | Token endpoint. |

### Profile

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/v1/profile/summary` | bearer | Redacted summary of claims visible under grant. |
| `POST` | `/v1/profile/query` | bearer | Query claims by namespace/key/domain. |
| `POST` | `/v1/profile/effective` | bearer | Resolve claims + modifiers under input context. |
| `POST` | `/v1/profile/propose-updates` | bearer | Submit updates; subject to writeback policy. |
| `POST` | `/v1/profile/confirm-updates` | bearer (elevated) | Confirm pending updates. |
| `POST` | `/v1/export` | bearer | Full export of profile in PPX format. |

#### Effective-profile response body

`POST /v1/profile/query` and `POST /v1/profile/effective` MUST return a
document valid against
[`effective-profile.schema.json`](../schemas/core/effective-profile.schema.json).

Required: `ppx_version`, `subject_id`, `provider_id`, `generated_at`,
`claims`, `applied_modifiers`.

Three notes, because each of these was a real ambiguity that two independent
implementations resolved differently:

- **This is not a stored Profile.** `profile.schema.json` describes a
  persisted document and requires `profile_id`. A resolved view is computed
  per grant, per context, and has no identity of its own — so `profile_id`
  here is OPTIONAL. Providers MAY omit it (withholding a stable cross-grant
  identifier is a legitimate privacy choice) and a grantee MUST NOT depend
  on it.
- **`applied_modifiers` is REQUIRED and MAY be empty.** An empty array means
  "no modifiers were applied". Omitting the field would be indistinguishable
  from "this provider does not report modifiers", which defeats the
  explainability the field exists for.
- **`generated_at` is REQUIRED** because context modifiers make the result
  time- and context-dependent. The same grant and context can legitimately
  resolve differently later, and a cached copy with no timestamp cannot be
  reasoned about.

Claims outside the grant are omitted silently. Their absence MUST NOT be
distinguishable from the claim not existing.

### Consent

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/v1/consent/grants` | bearer | List grants for the subject. |
| `POST` | `/v1/consent/revoke` | bearer (subject) | Revoke a grant by `grant_id`. |

### Audit

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/v1/audit/events` | bearer | Access log for the subject. |

### Derived views

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/v1/derived-views/{kind}` | bearer | Create a derived view of a given kind (e.g. `match`, `compatibility`, `recommendation_basis`). |

### Extensions

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `GET` | `/v1/extensions` | none | List supported extensions with versions. |

## Common response envelope

Successful PPX responses carrying claim data SHOULD include a `grant` block
echoing the scope used to evaluate the request, to enable client-side and
conformance-test auditing:

```json
{
  "profile_id": "ppx:profile:...",
  "claims": [ /* ... */ ],
  "grant": {
    "grant_id": "ppx:grant:...",
    "allowed_namespaces": ["core", "fragrance"],
    "allowed_claim_keys": [ /* ... */ ],
    "purposes": ["recommendation"]
  },
  "writeback": "none"
}
```

## Error shape

```json
{
  "error": "insufficient_scope",
  "error_description": "grant does not include key fragrance.occasion_bias",
  "grant_id": "ppx:grant:...",
  "details": { }
}
```

Canonical error codes:

- `invalid_token`
- `insufficient_scope`
- `cross_domain_denied`
- `writeback_forbidden`
- `writeback_pending`
- `grant_expired`
- `grant_revoked`
- `unknown_namespace`
- `unknown_extension`

## Rate limits

Not normatively specified in v0.1. Providers SHOULD advertise limits via
`RateLimit-*` response headers (draft-ietf-httpapi-ratelimit-headers).

## OpenAPI

Providers SHOULD publish an OpenAPI 3.1 document at `/openapi.json`
(advertised via discovery card `transport_bindings.http_api.openapi_uri`).
