<p align="center">
  <img src="site/docs/assets/logo.svg" alt="PPX logo" width="128" height="128"/>
</p>

# PPX — Preference Profile Exchange

> Portable, user-owned, consented preference and context profiles for agent ecosystems.

**Status:** Draft v0.1.0 — pre-standardization, pre-stable.

PPX defines a standard format and interaction model for representing, sharing,
querying, and updating user-owned preference/context profiles across applications
and agents — with first-class consent, provenance, and explainability.

It is designed to sit **beside** existing agent-interop standards, not replace them:

| Layer | Standard |
|---|---|
| Tool / data access | [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) |
| Agent-to-agent collaboration | [A2A](https://a2a-protocol.org/) |
| Live agent ↔ user-facing app | [AG-UI](https://docs.ag-ui.com/) |
| Generated declarative UI | [A2UI](https://a2ui.org/) |
| **User preference / context exchange** | **PPX** (this spec) |

## What's in this repo

- [`SPEC.md`](SPEC.md) — the normative specification document (v0.1)
- [`schemas/`](schemas/) — JSON Schemas (2020-12) for every PPX object
- [`examples/`](examples/) — valid payload examples for every schema
- [`conformance/`](conformance/) — executable conformance tests (pytest)
- [`bindings/`](bindings/) — how PPX rides over MCP, A2A, AG-UI, A2UI, and plain HTTP
- [`governance/`](governance/) — namespace registration, versioning, proposal process
- [`site/`](site/) — MkDocs Material source for the public documentation site

## Read the spec

Render the docs site locally:

```bash
cd site
pip install -r requirements.txt
mkdocs serve
```

Or read the raw normative document: [`SPEC.md`](SPEC.md).

## Run conformance tests against a provider

```bash
cd conformance
pip install -e .
PPX_PROVIDER_URL=https://your-provider.example.com pytest
```

## Positioning (the 30-second pitch)

> MCP standardizes tool and data access. A2A standardizes agent collaboration.
> AG-UI standardizes live app interaction. PPX standardizes the missing layer:
> **portable, user-owned preference and context profiles that agents can request,
> explain, and use with permission.**

## License

- Normative prose: [CC BY 4.0](LICENSE-SPEC)
- Schemas, examples, conformance code: [Apache 2.0](LICENSE-SCHEMAS)

## Contributing

PPX is a draft proposal. Early contributions — especially review of the consent
model, domain extensions, and binding mappings — are welcome. See
[`governance/PROPOSAL-TEMPLATE.md`](governance/PROPOSAL-TEMPLATE.md).
