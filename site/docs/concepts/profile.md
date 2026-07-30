# Profile

A **Profile** is a user-scoped collection of structured claims about
preferences, aversions, tendencies, and context modifiers.

## Minimal shape

```json
{
  "ppx_version": "0.1",
  "profile_id": "ppx:profile:...",
  "subject_id": "did:example:user-123",
  "provider_id": "ppx:provider:...",
  "created_at": "2026-04-06T18:05:00Z",
  "updated_at": "2026-04-20T09:14:00Z"
}
```

## Identity

A profile's `subject_id` is intentionally **identity-independent**. It MAY be
a DID, a UUID, or a provider-internal opaque ID. PPX does not specify a
canonical identity format; the aim is to let providers interoperate without
requiring a shared identity layer.

## Default policy

The profile's `default_policy` applies when no grant or per-claim policy
overrides it:

```json
{
  "default_policy": {
    "cross_domain_transfer": "deny",
    "inference_writeback": "review_required",
    "retention_days": 365
  }
}
```

## What goes *in* a profile

- **Claims** — the structured preferences ([concept](claim.md)).
- **Context modifiers** — how claims are interpreted under specific
  conditions ([concept](context-modifier.md)).
- **Consent grants** — who has scoped access ([concept](consent-grant.md)).
- **Extensions** — which namespaces the profile uses.

## What does NOT go in

- Raw memory.
- Chat transcripts.
- Biometric identity.
- High-impact claims (health, employment, housing, insurance, credit) —
  out of scope for v0.1.

## See also

- [Schema: profile.schema.json](https://ppx.dev/schemas/core/profile.schema.json)
- [Example: profile-basic.json](https://ppx.dev/examples/profile-basic.json)
