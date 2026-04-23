# Consent and trust

Consent is first-class in PPX. A provider MUST NOT assume that profile claims
are globally reusable across domains, across grantees, or across purposes.

## Deny by default

A grantee has no access until a grant exists — and has **only** the access
the grant specifies. There is no implicit read permission based on identity
alone.

## Scoped grants

A grant scopes access on six axes:

1. **Purposes** — recommendation, ranking, matching, explanation, etc.
2. **Domains** — fragrance, travel, media, etc.
3. **Namespaces** — core, fragrance, travel, etc.
4. **Claim keys** — specific keys within those namespaces.
5. **Operations** — read, query, propose_update, confirm_update, export.
6. **Time** — every grant has an `expires_at`.

See [`ConsentGrant` schema](../schemas/core/consent-grant.schema.json) for the
complete shape.

## Cross-domain transfer

The most sensitive pattern. Values:

- `deny` — default. No cross-domain reuse.
- `allow_with_review` — requires explicit user review at request time.
- `allow_if_same_provider` — permitted inside the same provider under other
  scoping.
- `allow` — unconditionally allowed under grant scope.

**v0.1 recommendation:** default to `deny`. Make exceptions explicit.

When a grantee requests cross-domain reuse, the provider exposes only
**mapped core traits**, never raw domain-specific keys. For example, a travel
agent granted `allow_with_review` receives:

- `core.novelty_tolerance`
- `core.social_energy_preference`
- `core.sensory_intensity_preference`

…but never `fragrance.family_preference`.

## Writeback policy

Values:

- `forbidden` — grantee cannot propose updates.
- `review_required` — default. Proposals create pending reviews for the user.
- `auto_for_low_risk` — narrow automatic writes with strict per-key opt-in.
- `allow` — full automatic writes.

**v0.1 recommendation:** default to `review_required`. Never silently
update `user_stated` claims.

## Redisclosure

Values:

- `forbidden` — grantee MUST NOT share claim values with third parties.
- `same_purpose_only` — may share only for the original purpose.
- `allow` — unrestricted onward sharing.

## Revocation

Grants can be revoked at any time and revocation MUST take effect within
60 seconds. Access tokens tied to a revoked grant become invalid; past audit
records persist.

## Provenance and honesty

Every claim carries a `source.kind` distinguishing:

- `user_stated` — the user said so.
- `observed` — derived from user behavior.
- `imported` — came in from another provider or source.
- `inferred` — produced by a model or rule.
- `derived_aggregate` — from aggregate patterns; MUST NOT be re-presented as
  user-stated.

User-facing surfaces **MUST** distinguish `user_stated` from all other kinds.
**Inferred claims MUST NOT be presented as facts.**

## Trust, in one sentence

> PPX is infrastructure when access is deny-by-default, consent is explicit
> and scoped, every claim carries provenance and confidence, cross-domain
> reuse is mediated by review, and users can see and revoke everything.
