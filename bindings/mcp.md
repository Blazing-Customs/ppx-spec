# Binding: PPX over MCP

**Target:** Model Context Protocol (MCP), spec version `2025-11-25`.

This document is normative for providers claiming the `mcp` transport binding
in their discovery card.

## Overview

A PPX provider MAY expose itself as an MCP server. Each PPX [core operation](../SPEC.md#9-core-operations)
is surfaced as an MCP tool of the same name. Profile data MAY additionally be
exposed via MCP **resources** (for read-only snapshots) where appropriate.

## Authentication

HTTP-based MCP transports **MUST** use OAuth 2.1 per the MCP authorization
model. PPX providers binding to MCP:

- MUST authenticate every request with a bearer access token.
- MUST issue access tokens bound to a specific PPX consent grant.
  The token SHOULD carry a `grant_id` claim (or equivalent) that the provider
  re-validates against current grant state on every request.
- MUST return `401 Unauthorized` with a `WWW-Authenticate` header on
  unauthenticated requests per RFC 9728.
- SHOULD use Resource Indicators (RFC 8707) to bind tokens to the provider's
  resource URI.

## Tool mapping

| PPX operation | MCP tool name | Brief |
|---|---|---|
| `get_profile_summary` | `ppx_get_profile_summary` | Returns redacted summary of claims visible to the caller. |
| `query_claims` | `ppx_query_claims` | Namespaced/keyed/domain/context query. |
| `get_effective_profile` | `ppx_get_effective_profile` | Claims + resolved context modifiers under input context. |
| `propose_updates` | `ppx_propose_updates` | Write-path subject to writeback policy. |
| `confirm_updates` | `ppx_confirm_updates` | User/authorized confirmation of pending updates. |
| `list_consent_grants` | `ppx_list_consent_grants` | Grants for the subject. |
| `revoke_consent_grant` | `ppx_revoke_consent_grant` | Revoke a specific grant. |
| `export_profile` | `ppx_export_profile` | Full export in PPX format. |

Each tool's input/output schema MUST be expressed as JSON Schema 2020-12 in
the server's tool listing, referencing the PPX core schemas published at
`/.well-known/ppx-card.json`.

## Resources

Providers MAY expose:

- `ppx://profile/{profile_id}/summary` — MCP resource returning the redacted
  summary.
- `ppx://profile/{profile_id}/effective?context=...` — parametric resource
  for effective profile.

Resources MUST honor the same grant scope as the equivalent tool call.

## Discovery

A PPX provider binding over MCP:

- MUST serve the MCP metadata document (SEP-1649 `/.well-known/mcp.json` when
  applicable; see current MCP spec).
- MUST also serve `/.well-known/ppx-card.json` with
  `transport_bindings.mcp.supported = true` and `transport_bindings.mcp.server_uri`
  set to the MCP server URI.

## Example discovery-card fragment

```json
{
  "transport_bindings": {
    "mcp": {
      "supported": true,
      "server_uri": "https://profiles.example.com/mcp"
    }
  },
  "auth": {
    "schemes": ["oauth2.1"],
    "authorization_endpoint": "https://profiles.example.com/oauth/authorize",
    "token_endpoint": "https://profiles.example.com/oauth/token"
  }
}
```

## Error handling

| Condition | OAuth2.1 / MCP response |
|---|---|
| No or invalid token | `401` + `WWW-Authenticate` |
| Token valid but grant expired/revoked | `401` (provider SHOULD include `error="invalid_token"`) |
| Scope violation (requested key/ns outside grant) | `403` + `error="insufficient_scope"` |
| Cross-domain transfer denied | `403` + PPX-specific error body |
| Writeback forbidden | `403` |
| Writeback pending review | `202` + `writeback: proposal_created` |

## Non-goals (this binding)

- This binding does not define MCP **prompts** for PPX; user-facing prompts
  belong in the AG-UI binding.
- This binding does not re-specify OAuth 2.1; follow the MCP authorization
  spec verbatim.
