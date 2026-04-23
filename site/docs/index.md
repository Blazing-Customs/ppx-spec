---
title: PPX — Preference Profile Exchange
description: Portable, user-owned, consented preference and context profiles for agent ecosystems.
---

# PPX — Preference Profile Exchange

**Portable, user-owned, consented preference and context profiles for agent ecosystems.**

!!! info "Status: Draft v0.1.0"
    PPX is an early-stage specification published for community review. Expect
    breaking changes before `1.0`. See [versioning policy](governance/versioning.md).

## The positioning

MCP standardizes tool and data access. A2A standardizes agent collaboration.
AG-UI standardizes live app interaction. **PPX standardizes the missing
layer: portable, user-owned preference and context profiles that agents can
request, explain, and use with permission.**

| Layer | Standard |
|---|---|
| Tool / data access | [MCP](https://modelcontextprotocol.io/) |
| Agent-to-agent collaboration | [A2A](https://a2a-protocol.org/) |
| Live agent ↔ app | [AG-UI](https://docs.ag-ui.com/) |
| Generated declarative UI | [A2UI](https://a2ui.org/) |
| **User preference / context** | **PPX** |

## Why PPX

Today, agents and apps personalize poorly because user context is fragmented,
static, locked into individual products, and often hidden from the user. Apps
repeatedly ask the same questions, infer things opaquely, and cannot safely
share user-approved context across domains.

PPX defines a small, extensible core for:

- **Portability** — profiles can move across applications and agents.
- **User ownership** — the user can inspect, export, correct, revoke.
- **Scoping** — access is limited by domain, purpose, allowed keys,
  operations, and time.
- **Explainability** — every non-trivial claim has provenance and confidence.
- **Extensibility** — domains can define vocabularies without destabilizing
  the core.

## What you can do with it

- A **fragrance app** asks for scent and sensory preferences, with a 30-day
  scoped grant.
- A **travel app** asks for climate and pace preferences, optionally
  reusing transferable core traits under user review.
- A **dating agent** receives a derived compatibility view, never the raw
  profile.
- A **finance app** (higher-risk, out of scope for v0.1) would require
  stricter policy than v0.1 defines.

The user always sees what was asked for, why, how long access lasts, whether
the app can write back changes, and what was inferred vs stated.

## Start here

- [Read the full specification](spec.md) (normative)
- [Getting started](getting-started.md) — run the conformance suite in 5 minutes
- [Explore the data model](data-model/schemas.md)
- [See the consent model](consent-and-trust.md)
- [Run a demo against the reference provider](getting-started.md#connect-to-the-reference-provider)

## Status

PPX v0.1.0 is a draft proposal. Breaking changes are expected before `1.0`.
The reference implementation — [`ppx-provider`](https://github.com/Blazing-Customs/ppx-provider) —
is under construction and proves the spec end-to-end, including the canonical
fragrance → travel cross-domain consent-transfer demo.

## License

- Normative prose: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Schemas & code: [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)
