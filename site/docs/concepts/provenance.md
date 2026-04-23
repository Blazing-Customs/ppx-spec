# Provenance & confidence

Every claim in PPX has a `source.kind` recording how the claim came to be,
and a `confidence` value recording how strongly the provider believes it
represents the subject.

## Provenance kinds

| Kind | Meaning |
|---|---|
| `user_stated` | The user explicitly stated the preference. |
| `observed` | Derived from observed user behavior. |
| `imported` | Imported from another PPX provider or compatible source. |
| `inferred` | Produced by a model or rule applied to other data. |
| `derived_aggregate` | Derived from aggregate patterns. MUST NOT be re-exposed as user-stated. |

**Rule:** user-facing surfaces MUST distinguish `user_stated` from all other
kinds. Inferred claims MUST NOT be presented as facts.

## Confidence

`confidence` is a value in `[0.0, 1.0]`. It expresses the provider's
confidence that the claim accurately represents the subject. It is **not** a
probability of truth in the world.

Rough bands (non-normative):

| Band | Meaning |
|---|---|
| 0.0–0.3 | Weak signal; show cautiously, flag for confirmation. |
| 0.3–0.6 | Moderate signal; surface with provenance and confidence visible. |
| 0.6–0.9 | Strong signal; still not fact. |
| 0.9–1.0 | Essentially confirmed — typically only for `user_stated` claims. |

## Stability

Independent of confidence, a claim has a `stability` level (`low`, `medium`,
`high`) expressing how stable the preference is expected to be over time.

## Evidence references

A claim MAY reference the evidence that informed it via `source.evidence_refs`.
Evidence payloads MAY remain private; only the reference and a privacy-safe
summary need be portable.

```json
{
  "evidence_id": "ppx:evidence:quiz:12",
  "kind": "pairwise_choice",
  "timestamp": "2026-03-18T12:10:22Z",
  "visibility": "provider_only",
  "summary": "User preferred scent A over scent B in a 'date night' context."
}
```

## See also

- [Claim concept](claim.md)
- [Consent & trust](../consent-and-trust.md)
