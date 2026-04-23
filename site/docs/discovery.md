# Discovery

A PPX provider advertises its capabilities at a well-known URL:

```
/.well-known/ppx-card.json
```

This follows the precedent of adjacent standards — MCP's `/.well-known/mcp.json`
(SEP-1649) and A2A's `/.well-known/agent-card.json`.

## Example

```json
{%
  include "../../examples/discovery-card.json"
%}
```

## Schema

The discovery card MUST validate against
[`schemas/core/discovery-card.schema.json`](https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/discovery-card.schema.json).

## Required fields

- `ppx_version` — spec version string.
- `provider_id` — URN identifying the provider.
- `name` — human name.
- `base_url` — HTTPS base URL.
- `capabilities` — what the provider supports.
- `supported_namespaces` — MUST include `core`.
- `supported_purposes` — at minimum one purpose.
- `default_policies` — defaults for `cross_domain_transfer` and
  `writeback_policy`.
- `auth.schemes` — non-empty list.

## Transport bindings

A provider's card advertises which transports are live:

```json
{
  "transport_bindings": {
    "mcp":      { "supported": true, "server_uri": "..." },
    "a2a":      { "supported": true, "agent_card_uri": "..." },
    "http_api": { "supported": true, "openapi_uri": "..." }
  },
  "ui": { "ag_ui_supported": true, "a2ui_supported": true }
}
```

See the [bindings section](bindings/mcp.md) for the binding contracts.
