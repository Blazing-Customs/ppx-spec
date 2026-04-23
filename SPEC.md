# Preference Profile Exchange (PPX) Specification

**Version:** 0.1.0-draft
**Status:** Draft — pre-standardization, pre-stable. Breaking changes expected before `1.0`.
**Date:** 2026-04-23
**Editors:** Blazing Customs / PPX contributors

---

## Abstract

This document defines the **Preference Profile Exchange (PPX)** specification:
a standard format and interaction model for representing, sharing, querying,
and updating portable, user-owned preference and context profiles across
applications and agents. PPX emphasizes first-class consent, provenance,
explainability, and extensibility, and is designed to be composable with
existing agent-interop standards — MCP, A2A, AG-UI, and A2UI — rather than to
replace any of them.

## Status of This Document

This is a draft specification published for community review. It is
**not** a stable or finalized standard. Readers, implementers, and adopters
should assume that any part of this document may change in incompatible ways
before version `1.0`.

## Conformance Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **NOT RECOMMENDED**, **MAY**, and
**OPTIONAL** in this document are to be interpreted as described in
[BCP 14][rfc2119] (RFC 2119 and RFC 8174) when, and only when, they appear in
all capitals, as shown here.

[rfc2119]: https://www.rfc-editor.org/info/bcp14

---

## 1. Purpose

The Preference Profile Exchange (PPX) specification defines a standard format
and interaction model for:

- representing a user-owned preference profile,
- granting scoped access to that profile,
- exchanging profile data across applications and agents,
- extending the profile with domain-specific vocabularies,
- explaining where profile claims came from and how confident the provider is
  in them.

PPX is intentionally scoped to:

- preferences,
- aversions,
- tendencies,
- context modifiers,
- provenance,
- confidence,
- consent,
- portability.

PPX does **not** attempt to model full identity, full memory, raw conversation
logs, or deterministic personhood.

### 1.1 Positioning

PPX is designed to be composable with existing agent-interop standards rather
than to compete with them. A conforming PPX provider MAY be exposed via any
binding defined in [§12 Bindings](#12-bindings):

- over **MCP** as a server offering profile tools and resources,
- over **A2A** as a remote "preference agent" callable by other agents,
- over **AG-UI** for live, event-based consent and review flows with end users,
- over **A2UI** for declarative, transport-agnostic UI components rendering
  profile cards, grant cards, and diffs,
- over plain **HTTP** as a REST API.

## 2. Goals

PPX aims to provide:

- **Portability** — profiles can move across applications and agents without
  lock-in.
- **User ownership** — the user can inspect, export, correct, and revoke.
- **Scoping** — access is limited by domain, purpose, allowed keys, operations,
  and time.
- **Explainability** — every non-trivial claim has provenance and confidence.
- **Extensibility** — domains can define vocabularies without destabilizing the
  core.
- **Time-awareness** — profiles can change, decay, and be refreshed.
- **Composability** — PPX rides over existing transports rather than inventing
  a new runtime.

## 3. Non-goals

PPX does **not** standardize:

- raw memory storage,
- biometric or legal identity,
- covert surveillance collection,
- unrestricted cross-domain profiling,
- deterministic personality or psychological classification,
- autonomous decisioning without application-level policy.

High-impact domains such as **health, employment, housing, insurance, and
credit** are explicitly **out of scope for v0.1**. Such domains SHOULD require
stricter policy than what this version defines, and MAY be addressed by a
future "high-impact domain" policy profile.

## 4. Core Concepts

### 4.1 Profile

A PPX **Profile** is a user-scoped collection of structured claims about
preferences, aversions, tendencies, and context modifiers.

### 4.2 Claim

A **Claim** is a machine-readable statement about the user. Examples:

- "prefers warm woody fragrances"
- "avoids chaotic interfaces"
- "tolerates medium novelty"
- "travel recommendations should weight climate strongly"

A claim MUST carry a `namespace`, a `key`, a `value`, a `source`, and a
`confidence`. See [§5.2](#52-claim-object).

### 4.3 Provenance

**Provenance** records how a claim came into being. PPX defines five
provenance kinds:

- `user_stated` — the user explicitly stated the preference.
- `observed` — derived from observed behavior.
- `imported` — imported from another PPX provider or compatible source.
- `inferred` — produced by a model or rule applied to other data.
- `derived_aggregate` — derived from aggregate patterns; MUST NOT be re-exposed
  as if user-stated.

An implementation MUST distinguish `user_stated` from all other provenance
kinds in any user-facing surface.

### 4.4 Confidence

**Confidence** is a value in the closed interval `[0.0, 1.0]` expressing the
provider's confidence that the claim accurately represents the subject. It is
**not** a probability of truth in the world. Providers MUST NOT present
inferred claims with high confidence as though they were stated facts.

### 4.5 Consent Grant

A **Consent Grant** is a first-class, user-controlled authorization that
defines **who** may access **which claims**, for **what purpose**, under
**what constraints**, and **for how long**. Grants are deny-by-default: a
grantee has no access until a grant exists, and has only the access the grant
specifies.

### 4.6 Domain Extension

A **Domain Extension** defines a vocabulary (namespace, claim keys, value
types, units, privacy guidance) for a specific vertical. Extensions are how
PPX scales to new domains without destabilizing the core.

### 4.7 Derived View

A **Derived View** is a scoped, often ephemeral projection of one or more
profiles produced for a specific task (for example, a compatibility vector
for dating, or a recommendation basis for fragrance). Derived views MUST NOT
re-export raw claims outside the scope of the grant that authorized them.

---

## 5. Data Model

All objects are JSON. Normative schemas are published under [`schemas/`](schemas/)
using [JSON Schema 2020-12][jsonschema-2020-12]. Where this document and a
schema disagree, the **schema is authoritative** for structural constraints
and this document is authoritative for semantics.

[jsonschema-2020-12]: https://json-schema.org/draft/2020-12/schema

Identifiers in PPX use a URN-style format: `ppx:<type>:<id>`. Providers MUST
NOT reuse identifiers across distinct objects.

### 5.1 Profile Object

```json
{
  "ppx_version": "0.1",
  "profile_id": "ppx:profile:7f4f7c87-9d98-4c9b-b8a0-0d86b1a8d502",
  "subject_id": "did:example:user-123",
  "provider_id": "ppx:provider:example-inc",
  "created_at": "2026-04-06T18:05:00Z",
  "updated_at": "2026-04-06T18:05:00Z",
  "default_policy": {
    "cross_domain_transfer": "deny",
    "inference_writeback": "review_required",
    "retention_days": 365
  },
  "claims": [],
  "context_modifiers": [],
  "consent_grants": [],
  "extensions": []
}
```

Required fields: `ppx_version`, `profile_id`, `subject_id`, `provider_id`,
`created_at`, `updated_at`.

Optional fields: `default_policy`, `claims`, `context_modifiers`,
`consent_grants`, `extensions`.

### 5.2 Claim Object

```json
{
  "claim_id": "ppx:claim:001",
  "type": "preference",
  "namespace": "core",
  "key": "novelty_tolerance",
  "value": 0.62,
  "value_type": "float",
  "units": "normalized_0_1",
  "polarity": "positive",
  "confidence": 0.78,
  "stability": "medium",
  "source": {
    "kind": "inferred",
    "origin": "choice_model_v3",
    "evidence_refs": [
      "ppx:evidence:quiz:12",
      "ppx:evidence:behavior:93"
    ]
  },
  "explanation": {
    "summary": "User tends to prefer moderate novelty over highly familiar or highly disruptive options."
  },
  "applicability": {
    "domains": ["fragrance", "travel", "media"],
    "contexts": ["default"]
  },
  "lifecycle": {
    "last_confirmed_at": "2026-03-20T15:00:00Z",
    "expires_at": "2026-09-20T15:00:00Z",
    "decay_policy": "linear"
  },
  "review": {
    "user_visible": true,
    "user_editable": true,
    "review_status": "pending_confirmation"
  }
}
```

Allowed `type` values in v0.1: `preference`, `aversion`, `tendency`,
`constraint`, `setting`, `derived_signal`.

Allowed `stability` values: `low`, `medium`, `high`.

Allowed `review_status` values: `unreviewed`, `pending_confirmation`,
`confirmed`, `rejected`.

Allowed `source.kind` values: `user_stated`, `observed`, `imported`,
`inferred`, `derived_aggregate`.

`confidence` MUST be in `[0.0, 1.0]`.

### 5.3 Context Modifier Object

Context modifiers alter how claims SHOULD be interpreted under specific
conditions.

```json
{
  "modifier_id": "ppx:modifier:014",
  "namespace": "core",
  "key": "climate_heat_humidity_bias",
  "effect_type": "weight_adjustment",
  "targets": [
    "fragrance.projection_preference",
    "fragrance.freshness_preference"
  ],
  "condition": { "climate": "hot_humid" },
  "effect": {
    "increase": ["freshness_preference"],
    "decrease": ["heavy_projection_preference"]
  },
  "confidence": 0.81,
  "source": { "kind": "observed", "origin": "seasonal_behavior_log" }
}
```

Core recommended context dimensions in v0.1:

- `climate`, `season`, `time_of_day`, `occasion`, `social_context`,
  `stress_level`, `budget_sensitivity`, `time_horizon`.

### 5.4 Evidence Reference

Evidence payloads MAY remain private while still being referenceable. PPX
does not require evidence payloads to be portable, only evidence **references
and summaries**.

```json
{
  "evidence_id": "ppx:evidence:quiz:12",
  "kind": "pairwise_choice",
  "timestamp": "2026-03-18T12:10:22Z",
  "visibility": "provider_only",
  "summary": "User preferred scent A over scent B in a 'date night' context."
}
```

Allowed `visibility` values: `public`, `grantee_only`, `provider_only`.

### 5.5 Derived View

A derived view is a projection produced for a particular task. It MUST NOT
include raw claim values outside the scope granted, and SHOULD include an
explanation surface suitable for user review.

---

## 6. Consent Model

Consent is first-class. A conforming PPX provider **MUST NOT** assume that
profile claims are globally reusable across domains, across grantees, or
across purposes.

### 6.1 Consent Grant Object

```json
{
  "grant_id": "ppx:grant:222",
  "subject_id": "did:example:user-123",
  "grantee_id": "did:example:agent:fragrance-app",
  "status": "active",
  "granted_at": "2026-04-06T18:10:00Z",
  "expires_at": "2026-05-06T18:10:00Z",
  "purposes": ["recommendation", "ranking", "explanation"],
  "allowed_domains": ["fragrance"],
  "allowed_namespaces": ["core", "fragrance"],
  "allowed_claim_keys": [
    "novelty_tolerance",
    "fragrance.family_preference",
    "fragrance.intensity_preference"
  ],
  "allowed_operations": ["read", "propose_update"],
  "cross_domain_transfer": "deny",
  "writeback_policy": "review_required",
  "redisclosure": "forbidden",
  "audit": {
    "log_access": true,
    "notify_on_writeback": true
  }
}
```

Allowed `status` values: `active`, `expired`, `revoked`, `pending`.

### 6.2 Consent Rules

A conforming PPX provider **MUST**:

1. Default to deny for any access not covered by an active grant.
2. Require an explicit grant per grantee; grants are not transferable.
3. Scope grants by at least domain, namespace, and purpose.
4. Enforce `expires_at`; an expired grant MUST NOT authorize new access.
5. Enforce `writeback_policy`; a grant with writeback `forbidden` MUST reject
   updates from the grantee.
6. Enforce `redisclosure`; a grant with redisclosure `forbidden` MUST prohibit
   the grantee from re-exposing claim values to third parties.
7. Support revocation; revoked grants MUST immediately deny further access.

### 6.3 Purpose Values

Recommended `purposes` in v0.1:

- `recommendation`, `ranking`, `matching`, `simulation`, `summarization`,
  `personalization`, `explanation`, `propose_update`.

### 6.4 Operation Values

Recommended `allowed_operations` values:

- `read`, `query`, `propose_update`, `confirm_update`, `export`.

### 6.5 Cross-domain Transfer

Allowed `cross_domain_transfer` values:

- `deny` — cross-domain reuse is prohibited.
- `allow_with_review` — permitted only with explicit user review at request
  time.
- `allow_if_same_provider` — permitted within the same provider if other
  grant scoping allows it.
- `allow` — unconditionally allowed under grant scope.

v0.1 providers **SHOULD** default to `deny`.

### 6.6 Writeback Policy

Allowed `writeback_policy` values:

- `forbidden`, `review_required`, `auto_for_low_risk`, `allow`.

v0.1 providers **SHOULD** default to `review_required`.

---

## 7. Discovery

A provider **MAY** publish a discovery document at:

```
/.well-known/ppx-card.json
```

This path follows the precedent established by adjacent agent-interop
standards (for example, MCP's `/.well-known/mcp.json` proposal).

### 7.1 Discovery Card Shape

```json
{
  "ppx_version": "0.1",
  "provider_id": "ppx:provider:example-inc",
  "name": "Example Preference Provider",
  "base_url": "https://profiles.example.com",
  "capabilities": {
    "profile_read": true,
    "claim_query": true,
    "consent_management": true,
    "propose_update": true,
    "export": true,
    "delete": true,
    "audit_log": true
  },
  "supported_namespaces": ["core", "fragrance", "media"],
  "supported_purposes": [
    "recommendation", "ranking", "matching", "explanation", "propose_update"
  ],
  "default_policies": {
    "cross_domain_transfer": "deny",
    "writeback_policy": "review_required"
  },
  "auth": { "schemes": ["oauth2", "openid_connect"] },
  "signing": { "profile_signatures": false, "grant_signatures": false },
  "transport_bindings": {
    "mcp": {
      "supported": true,
      "server_uri": "https://profiles.example.com/mcp"
    },
    "a2a": {
      "supported": true,
      "agent_card_uri": "https://profiles.example.com/.well-known/agent-card.json"
    },
    "http_api": {
      "supported": true,
      "openapi_uri": "https://profiles.example.com/openapi.json"
    }
  },
  "ui": { "ag_ui_supported": true, "a2ui_supported": true }
}
```

A conforming provider's discovery card **MUST** validate against
[`schemas/core/discovery-card.schema.json`](schemas/core/discovery-card.schema.json).

---

## 8. Extension Model

PPX is intentionally small at the core. Domain-specific vocabularies are
defined through **namespaces** and **extension descriptors**.

### 8.1 Extension Requirements

Each extension **MUST** define:

- namespace name,
- semantic meaning of each key,
- allowed value types,
- units (where applicable),
- provenance guidance,
- confidence guidance,
- privacy considerations,
- whether cross-domain use is `recommended`, `discouraged`, or `forbidden`.

### 8.2 Extension Descriptor Shape

```json
{
  "namespace": "fragrance",
  "version": "0.1",
  "title": "Fragrance Preference Extension",
  "keys": [
    {
      "key": "family_preference",
      "value_type": "map<string,float>",
      "description": "Relative affinity for fragrance families."
    },
    {
      "key": "intensity_preference",
      "value_type": "float",
      "units": "normalized_0_1"
    },
    {
      "key": "projection_tolerance",
      "value_type": "float",
      "units": "normalized_0_1"
    },
    { "key": "occasion_bias", "value_type": "map<string,float>" }
  ],
  "privacy_guidance": {
    "cross_domain_use": "discouraged_without_review"
  }
}
```

### 8.3 Core Namespace

The `core` namespace **SHOULD** remain intentionally generic. v0.1 core keys
include:

- `novelty_tolerance`
- `risk_tolerance`
- `regret_sensitivity`
- `sensory_intensity_preference`
- `social_energy_preference`
- `decision_speed_preference`
- `ambiguity_tolerance`
- `budget_sensitivity`
- `explanation_depth_preference`
- `conversation_depth_preference`

All core keys **MUST** take values in `[0.0, 1.0]` with `units` of
`normalized_0_1`.

### 8.4 Extension Governance

An eventual open-standard body **SHOULD** require:

- unique namespace registration,
- public schema and privacy notes,
- at least two interoperable implementations before a "stable" status.

See [`governance/NAMESPACE-REGISTRATION.md`](governance/NAMESPACE-REGISTRATION.md).

---

## 9. Core Operations

PPX does not mandate a single wire protocol. The following logical operations
are defined and MUST be realizable across any conforming transport binding
(see [§12](#12-bindings)):

| Operation | Summary |
|---|---|
| `get_profile_summary` | Return a redacted summary of profile claims visible to the requester. |
| `query_claims` | Query a subset of claims by namespace, key, domain, or context. |
| `get_effective_profile` | Return claims plus active context modifiers resolved for a supplied context. |
| `propose_updates` | Request that new or modified claims be added; subject to writeback policy. |
| `confirm_updates` | User or authorized actor confirms pending proposals. |
| `list_consent_grants` | List active and expired grants for the subject. |
| `revoke_consent_grant` | Revoke an existing grant. |
| `export_profile` | Export profile, grants, and supported extensions in PPX format. |

Example input to `get_effective_profile`:

```json
{
  "context": {
    "climate": "hot_humid",
    "occasion": "date_night",
    "time_of_day": "evening"
  }
}
```

---

## 10. Security and Privacy Requirements

A conforming PPX implementation **MUST**:

1. Authenticate the requester before evaluating any grant.
2. Evaluate each access against an active consent grant.
3. Audit access to any non-public claim.
4. Distinguish inferred claims from stated claims in all user-facing surfaces.
5. Support revocation with immediate effect (within 60 seconds).
6. Support export and deletion flows where the deploying platform's law and
   policy allow.
7. Use transport-level authentication (OAuth 2.1 or equivalent) when exposed
   over HTTP-based transports.

A conforming PPX implementation **MUST NOT**:

1. Silently widen domain, namespace, purpose, or key access beyond what the
   grant specifies.
2. Auto-write inferred high-impact claims without review.
3. Present inference as fact.
4. Leak restricted evidence across grantees.

High-impact domains (see [§3 Non-goals](#3-non-goals)) **SHOULD** require
stricter policy than v0.1 defines.

---

## 11. UX Requirements

When a PPX implementation exposes user-facing review, the UI **SHOULD**:

- show what is stated vs inferred,
- show confidence,
- show source summary,
- show `last_confirmed_at` / `expires_at`,
- show who can currently access each claim category,
- allow revoke, correct, and confirm actions.

This maps naturally onto AG-UI for live state sync and A2UI for declarative
cards, forms, and diffs. See [§12.3](#123-ag-ui-binding) and
[§12.4](#124-a2ui-binding).

---

## 12. Bindings

Normative binding documents live under [`bindings/`](bindings/). This section
summarizes them.

### 12.1 MCP Binding

PPX operations MAY be exposed as MCP tools and resources. Core operations map
to MCP tool names of the same name. Authentication follows MCP's authorization
model (OAuth 2.1 for HTTP-based transports). See [`bindings/mcp.md`](bindings/mcp.md).

### 12.2 A2A Binding

A PPX provider MAY be exposed as an A2A-callable remote agent ("preference
agent"). The provider's A2A agent card advertises PPX skills such as
`get_effective_profile`, `compatibility_view`, and `scoped_query`. See
[`bindings/a2a.md`](bindings/a2a.md).

### 12.3 AG-UI Binding

Live user-facing PPX flows — consent prompts, claim review, audit inspection —
SHOULD use AG-UI event streams. Recommended event types: `STATE_SNAPSHOT`,
`STATE_DELTA`, `INTERRUPT` (for consent prompts), `TEXT_MESSAGE_*` (for
explanations), `TOOL_CALL_*` (for propose/confirm flows). See
[`bindings/ag-ui.md`](bindings/ag-ui.md).

### 12.4 A2UI Binding

Declarative UI components rendering PPX objects — `ClaimCard`, `GrantCard`,
`ProfileDiffView`, `ConsentRequestForm` — SHOULD follow A2UI v0.8 flat
adjacency-list structure with JSON-Pointer data bindings. See
[`bindings/a2ui.md`](bindings/a2ui.md).

### 12.5 HTTP Binding

The plain REST binding defines endpoints:

```
GET  /.well-known/ppx-card.json
GET  /v1/profile/summary
POST /v1/profile/query
POST /v1/profile/effective
POST /v1/profile/propose-updates
POST /v1/profile/confirm-updates
GET  /v1/consent/grants
POST /v1/consent/revoke
GET  /v1/audit/events
POST /v1/derived-views/{kind}
GET  /v1/extensions
POST /v1/export
POST /oauth/authorize
POST /oauth/token
```

See [`bindings/http.md`](bindings/http.md).

---

## 13. Three Example Flows

### 13.1 Flow 1 — Single-domain recommendation (fragrance)

**Actors:** user, PPX provider, fragrance agent.

1. Fragrance agent requests a grant for `core` and `fragrance` namespaces,
   purpose `recommendation`.
2. User approves a 30-day grant, domain `fragrance` only.
3. Agent calls `get_effective_profile` with
   `{climate: hot_humid, occasion: date_night}`.
4. Provider returns moderate novelty tolerance, high freshness preference,
   medium projection tolerance, low sweetness preference.
5. Agent ranks fragrances and surfaces an explanation.
6. Agent calls `propose_updates` with an observed preference; provider stores
   it with `review_status: pending_confirmation`.

### 13.2 Flow 2 — Cross-domain transfer with review (fragrance → travel)

**Actors:** user, PPX provider, travel agent.

1. Travel agent requests `core` namespace, purpose `recommendation`,
   operation `read`, with cross-domain transfer from fragrance-derived signals.
2. Provider finds `cross_domain_transfer = deny` by default and prompts user.
3. User approves `allow_with_review`.
4. Provider exposes **only mapped core traits** (`novelty_tolerance`,
   `sensory_intensity_preference`, `social_energy_preference`); raw
   `fragrance.family_preference` is NOT exposed.
5. Travel agent recommends destinations with an explanation surface.

This is the canonical cross-domain reuse pattern. Reuse is mediated through
policy, user review, redaction, and trait mapping — never by raw export.

### 13.3 Flow 3 — Agent-to-agent scoped matching (dating)

**Actors:** user, dating agent, PPX provider (or preference agent),
optional remote compatibility agent.

1. Dating agent requests purpose `matching` for a narrow key set.
2. User approves a one-time grant.
3. Compatibility agent calls `query_claims` (or receives a
   derived-matching view).
4. Provider returns **only** normalized vectors, confidence, and
   explanation-friendly summaries.
5. Grant expires after the matching session. No unrestricted export occurs.

---

## 14. Conformance Levels

A conforming PPX provider declares the highest level it supports.

| Level | Name | Adds |
|---|---|---|
| L1 | Portable Read | Profile export, claim read, consent-grant evaluation. |
| L2 | Context-aware | Context modifiers, effective-profile resolution, provenance, confidence. |
| L3 | Interactive | Propose/confirm updates, consent-management UI, audit log, structured explanations. |
| L4 | Multi-agent | Derived scoped views, agent-to-agent usage, ephemeral grants, extension interoperability. |

See [`governance/CONFORMANCE-LEVELS.md`](governance/CONFORMANCE-LEVELS.md).

---

## 15. Open Questions for v0.2

- Should PPX define a standard derived-vector format?
- Should grants be signable/verifiable artifacts (e.g. JWTs with profile
  binding)?
- Should there be a standard "high-impact domain" policy profile?
- Should extensions be able to declare mandatory user review for specific
  keys?
- Should PPX support revocable pseudonymous profile links across providers?
- Should there be a standard "profile diff" object for time-based change
  tracking?

---

## 16. Versioning

The normative spec document is tracked by `MAJOR.MINOR.PATCH-STAGE` with dated
releases. Schemas are tracked by semver. See
[`governance/VERSIONING.md`](governance/VERSIONING.md).

## 17. Governance

See [`governance/`](governance/):

- [`NAMESPACE-REGISTRATION.md`](governance/NAMESPACE-REGISTRATION.md)
- [`VERSIONING.md`](governance/VERSIONING.md)
- [`PROPOSAL-TEMPLATE.md`](governance/PROPOSAL-TEMPLATE.md)
- [`CONFORMANCE-LEVELS.md`](governance/CONFORMANCE-LEVELS.md)

## 18. Appendix A — Glossary

- **Claim** — a machine-readable statement about a subject's preference,
  aversion, tendency, constraint, setting, or derived signal.
- **Context modifier** — an object altering how claims should be interpreted
  under specific conditions.
- **Consent grant** — a user-authorized scoped access to claims.
- **Derived view** — a task-scoped projection of one or more profiles.
- **Discovery card** — a `/.well-known/ppx-card.json` document advertising
  provider capability.
- **Evidence reference** — a pointer to supporting data for a claim; payload
  MAY remain private.
- **Extension** — a domain-specific vocabulary registered under a unique
  namespace.
- **Profile** — a user-scoped collection of claims, context modifiers, and
  consent grants.
- **Provider** — a system that hosts and serves PPX profiles.
- **Grantee** — an app, agent, or service authorized by a consent grant.

## 19. Appendix B — References

- [BCP 14 / RFC 2119 / RFC 8174 — Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/info/bcp14)
- [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Agent-to-Agent Protocol (A2A)](https://a2a-protocol.org/)
- [AG-UI](https://docs.ag-ui.com/)
- [A2UI v0.8](https://a2ui.org/specification/v0.8-a2ui/)
- [RFC 8615 — Well-Known URIs](https://www.rfc-editor.org/rfc/rfc8615)
- [RFC 8141 — URNs](https://www.rfc-editor.org/rfc/rfc8141)
- [OAuth 2.1 (draft)](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-13)
