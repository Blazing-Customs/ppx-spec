---
title: Implementations
description: Two independent implementations of PPX v0.1, both passing the same conformance suite.
---

# Implementations

A specification with one implementation is a description of that
implementation. The bar for taking a spec seriously is **two independent
implementations that pass the same conformance suite** — because that is what
demonstrates the document is complete enough for someone to build from, rather
than a write-up of whatever the first codebase happened to do.

PPX v0.1 has two.

| | Reference provider | PHP provider |
| --- | --- | --- |
| **Language** | Python | PHP 8.1 |
| **Stack** | FastAPI + PostgreSQL + Keycloak + Next.js | Front-controller PHP + SQLite |
| **Identity** | Keycloak (OIDC) | Self-issued RS256 grant tokens |
| **Dependencies** | Docker Compose, 4 services | None beyond stock PHP (`openssl`, `pdo_sqlite`, `json`) |
| **Runs on** | A machine you administer | Commodity shared hosting |
| **Conformance** | Schema suite passes offline | **18/18, run against the live deployment** |

Both were written against [the specification](spec.md) and both are checked by
the same [conformance suite](conformance.md). Neither shares a line of code with
the other.

## What the second implementation established

The PHP provider was written to answer a narrow question — *can a conforming
provider run on ordinary shared hosting?* — and it settled three broader ones.

**The spec does not require a heavyweight stack.** The reference provider needs
four services and a machine to run them on. That is a property of the reference
provider, not of PPX. The normative auth surface is one hard requirement — an
expired grant MUST NOT authorize new access — plus "OAuth 2.1 or equivalent"
and a bearer token. Keycloak is one way to satisfy that, not the way.

**The spec is implementable from the document alone.** Every endpoint, status
code, and payload shape in the PHP provider was derived from `SPEC.md`, the
HTTP binding, and the eleven schemas. Where the specification was precise, the
implementation followed it directly; the conformance suite then confirmed the
result interoperates.

**The floor is lower than it looked.** The whole provider is a few hundred lines
of dependency-free PHP over a file-backed database. If that is the cost of
entry, a provider is something an application can add, not a system it has to
adopt.

## Conformance results

The suite is the same one in this repository, run over public HTTPS against the
deployed PHP provider:

```
18 passed
```

with no skipped tests. That covers discovery-card validity, deny-by-default for
unauthenticated and invalid tokens, expired-grant rejection, scope redaction,
revocation taking effect, cross-domain denial, write-back proposals under
`review_required`, refusal under `forbidden`, and the schema round-trips.

!!! note "What conformance does and does not mean"

    Passing L1 means a provider answers correctly on the behaviours the suite
    exercises. It is not a security audit, and it is not a claim that either
    implementation is production-ready. PPX is `v0.1.0-draft`; both providers
    serve demonstration data only.

## Writing a third

That is the useful next step, and the spec is more likely to improve from it
than from more work on either existing provider.

Start with the [HTTP binding](bindings/http.md), serve a
[discovery card](data-model/schemas.md), then run:

```bash
git clone https://github.com/Blazing-Customs/ppx-spec
pip install -e ppx-spec/conformance
PPX_PROVIDER_URL=https://your-provider.example pytest ppx-spec/conformance
```

The provider-backed tests need grant-scoped tokens supplied through the
environment; `conformance/README.md` lists them. If something in the
specification is ambiguous enough that you had to guess, that is a spec bug —
please [open an issue](https://github.com/Blazing-Customs/ppx-spec/issues).
