# Getting started

## 1. Read the spec

Start with the normative document: [Specification](spec.md). Key sections:

- [§4 Core concepts](spec.md#4-core-concepts) — Profile, Claim, Grant, etc.
- [§5 Data model](spec.md#5-data-model) — JSON shapes.
- [§6 Consent model](spec.md#6-consent-model) — the heart of PPX.
- [§13 Three example flows](spec.md#13-three-example-flows) — single-domain,
  cross-domain, and agent-to-agent.

## 2. Inspect the schemas

All schemas live under [`schemas/`][schemas] in the repo. Each object has a
corresponding JSON Schema 2020-12 file:

- [`profile.schema.json`][profile]
- [`claim.schema.json`][claim]
- [`consent-grant.schema.json`][grant]
- [`discovery-card.schema.json`][disc]

[schemas]: https://github.com/Blazing-Customs/ppx-spec/tree/main/schemas
[profile]: https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/profile.schema.json
[claim]: https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/claim.schema.json
[grant]: https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/consent-grant.schema.json
[disc]: https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/core/discovery-card.schema.json

## 3. Run the conformance suite

```bash
git clone https://github.com/Blazing-Customs/ppx-spec.git
cd ppx-spec/conformance
pip install -e .

# Schema-only (no provider needed)
pytest -m schema
```

Against a live provider:

```bash
PPX_PROVIDER_URL=https://your-provider.example.com \
PPX_PROVIDER_TOKEN=<bearer-token> \
pytest -m level1
```

## 4. Connect to the reference provider {#connect-to-the-reference-provider}

The canonical reference implementation lives at
[`ppx-provider`](https://github.com/Blazing-Customs/ppx-provider).

It brings up the full stack via `docker-compose`:

- FastAPI backend
- Postgres + Keycloak (OIDC + OAuth2.1 authorization server)
- Next.js frontend (consent screens, profile inspector, audit)
- MCP binding + A2A adapter
- Two demo apps (fragrance + travel)

See its README for the local-boot walkthrough.

## 5. Stand up a minimal provider yourself

A minimal PPX provider needs:

1. An auth layer (OIDC + OAuth 2.1).
2. A datastore for profiles, claims, grants, and audit events.
3. A grant engine that enforces scope/purpose/domain/key/op on every request.
4. The eight core HTTP endpoints ([`bindings/http.md`](bindings/http.md)).
5. A discovery card at `/.well-known/ppx-card.json`.

That's enough for **Level 1** conformance.
