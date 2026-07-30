---
title: Bindings
description: How PPX maps onto MCP, A2A, AG-UI, A2UI, and plain HTTP.
---

# Bindings

The [specification](../spec.md) defines PPX's data model and operations
independently of any transport. A **binding** says how those operations are
carried over one concrete protocol, so that two implementations that pick the
same binding interoperate without further negotiation.

| Binding | Use it when |
| --- | --- |
| [HTTP](http.md) | The baseline. Every conforming provider MUST implement it; the others are layered on top. |
| [MCP](mcp.md) | An LLM tool-calling client should read preferences as tools/resources. |
| [A2A](a2a.md) | Two autonomous agents exchange profile context directly. |
| [AG-UI](ag-ui.md) | A UI needs live consent prompts and grant events streamed to it. |
| [A2UI](a2ui.md) | An agent drives a rendered surface it does not own. |

All bindings share the same [consent model](../consent-and-trust.md): a
binding changes the envelope, never the scope of what a grant permits.

Conformance is declared per binding — see [Conformance levels](../conformance.md).
