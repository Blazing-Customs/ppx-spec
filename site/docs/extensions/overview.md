# Extensions

PPX is intentionally small at the core. **Namespaces** and **extension
descriptors** carry domain-specific vocabulary.

## Built-in namespaces (v0.1)

| Namespace | Purpose |
|---|---|
| [`core`](core.md) | Cross-cutting, domain-independent traits. |
| [`fragrance`](fragrance.md) | Scent preference vocabulary. |
| [`travel`](travel.md) | Travel and environment preference vocabulary. |

## When to define a new namespace

Register a new namespace when:

- A domain has signals that don't map cleanly into `core`.
- You need domain-specific value types (e.g. `map<string,float>` over
  fragrance families).
- You want to publish privacy guidance specific to the domain.

## How to register one

1. Write a descriptor and schema under `schemas/extensions/<namespace>.schema.json`.
2. Draft a proposal in `governance/proposals/<namespace>.md` based on
   [`PROPOSAL-TEMPLATE.md`](../governance/proposal-template.md).
3. Open a PR. See [Namespace registration](../governance/namespace-registration.md).

## Privacy guidance categories

Every extension MUST specify `privacy_guidance.cross_domain_use`:

- `recommended` — safely cross-cutting (typical for `core`).
- `discouraged_without_review` — cross-domain reuse requires user review.
- `forbidden` — MUST NOT cross domains.

## Out of scope for v0.1

Namespaces covering **health, employment, housing, insurance, or credit**
MUST NOT be registered in v0.1. They require a future high-impact-domain
policy profile.
