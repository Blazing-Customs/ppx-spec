# Binding: PPX over A2A

**Target:** Agent-to-Agent (A2A) Protocol, v1.x.

This document is normative for providers claiming the `a2a` transport binding
in their discovery card.

## Overview

A PPX provider MAY expose itself as an A2A-callable remote agent ("preference
agent"). Other agents may invoke its skills to request scoped profile views,
propose updates, or request derived views (e.g. a compatibility vector).

## Agent card

The preference agent **MUST** publish an A2A agent card at:

```
/.well-known/agent-card.json
```

with skills at minimum including:

- `get_effective_profile` — scoped claim resolution under a context.
- `compatibility_view` — derived matching view for dating/compat use.
- `recommendation_basis` — derived view listing claim keys contributing to
  a recommendation (for explanation surfaces).
- `propose_update` — subject to writeback policy.

Example agent-card fragment:

```json
{
  "name": "PPX Preference Agent",
  "description": "Scoped preference/context provider following the PPX specification.",
  "url": "https://profiles.example.com/a2a",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "authentication": {
    "schemes": ["bearer"],
    "metadata": {
      "tokenUrl": "https://profiles.example.com/oauth/token",
      "scopes": ["ppx:read", "ppx:propose_update"]
    }
  },
  "skills": [
    {
      "id": "get_effective_profile",
      "name": "Get effective profile",
      "description": "Return scoped claims + resolved context modifiers under a supplied context.",
      "tags": ["ppx", "profile", "preference"]
    },
    {
      "id": "compatibility_view",
      "name": "Compatibility view",
      "description": "Return a derived compatibility view for a pair of subjects. Does not expose raw claims."
    }
  ]
}
```

## Authentication

A2A binding **MUST** authenticate every request with a bearer token bound to
a PPX consent grant. See [§6 Consent Model](../SPEC.md#6-consent-model).

## Message shape

A2A uses JSON-RPC 2.0. A PPX request body maps as follows:

- `method` — the PPX operation (`get_effective_profile`, `compatibility_view`,
  etc.).
- `params` — the operation input (matches the HTTP binding's request body
  schema for the equivalent endpoint).

A PPX response body maps back into the A2A `result` field, and errors into
A2A `error` with codes per MCP/A2A conventions.

## Non-goals

- This binding does not specify A2A-to-A2A delegation chains; a preference
  agent MUST NOT delegate a grant to another A2A agent without user consent.
- This binding does not define long-running task semantics beyond the A2A
  task lifecycle. PPX operations are generally short-lived.
