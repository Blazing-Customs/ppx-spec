# Namespace Registration

PPX keeps its core vocabulary small and lets domains extend it via namespaces.
This document defines the registration process.

## Requirements for a registered namespace

A candidate namespace **MUST**:

1. Have a lowercase, snake_case identifier matching `^[a-z][a-z0-9_]*$` and
   be distinct from `core` and from all other registered namespaces.
2. Publish an **Extension Descriptor** (see
   [`SPEC.md §8.2`](../SPEC.md#82-extension-descriptor-shape)) as a JSON Schema
   or JSON file in this repository under `schemas/extensions/<namespace>.schema.json`.
3. Specify, for each key: semantic meaning, value type, units (if any),
   provenance guidance, and confidence guidance.
4. Specify `privacy_guidance.cross_domain_use` ∈
   `{recommended, discouraged_without_review, forbidden}`.
5. Include privacy notes covering high-impact classification and correlation
   risk.

A candidate namespace **SHOULD**:

- Provide at least one example profile and grant demonstrating typical use.
- Define at least one recommended context modifier if the domain has common
  context effects.
- Reuse `core` keys where the signal is generic, rather than duplicating them.

## Stability levels

| Level | Meaning |
|---|---|
| `experimental` | Published but not recommended for production; shape may change freely. |
| `draft` | Candidate for stabilization; at least one reference implementation exists. |
| `stable` | At least two interoperable implementations; breaking changes require a major version. |

A namespace moves from `draft` to `stable` only after:

1. At least **two** independent interoperable implementations.
2. All conformance tests relevant to the namespace pass against both.
3. A 30-day comment period on the proposal PR with no unresolved blocking
   issues.

## Registration process

1. Open a PR adding `schemas/extensions/<namespace>.schema.json` and any
   related examples.
2. Include a short proposal document in `governance/proposals/<namespace>.md`
   based on [`PROPOSAL-TEMPLATE.md`](PROPOSAL-TEMPLATE.md).
3. Flag privacy/security sensitivities explicitly.
4. Wait for editor review and (for `stable` promotion) the two-implementation
   bar.

## High-impact domain policy

Namespaces covering **health, employment, housing, insurance, or credit**
MUST NOT be registered in v0.1. They require a future "high-impact domain"
policy profile not yet defined.
