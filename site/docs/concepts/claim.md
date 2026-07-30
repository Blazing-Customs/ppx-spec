# Claim

A **Claim** is a machine-readable statement about the subject's preference,
aversion, tendency, constraint, setting, or derived signal.

## Required fields

- `claim_id`
- `type` — one of `preference`, `aversion`, `tendency`, `constraint`,
  `setting`, `derived_signal`.
- `namespace` — `core` or a registered extension.
- `key`
- `value`
- `confidence` — `[0.0, 1.0]`.
- `source` — provenance block.

## Example

```json
{
  "claim_id": "ppx:claim:c-001",
  "type": "preference",
  "namespace": "core",
  "key": "novelty_tolerance",
  "value": 0.62,
  "value_type": "float",
  "units": "normalized_0_1",
  "confidence": 0.78,
  "stability": "medium",
  "source": {
    "kind": "inferred",
    "origin": "onboarding_quiz_v1",
    "evidence_refs": ["ppx:evidence:quiz:12"]
  }
}
```

## Value types

| `value_type` | Shape |
|---|---|
| `float` | Number in `[0.0, 1.0]` when `units = normalized_0_1`. |
| `int` | Integer. |
| `bool` | `true` / `false`. |
| `string` | String; MAY be constrained via extension `allowed_values`. |
| `string_list` | Array of strings. |
| `map<string,float>` | Object mapping string keys to floats. |

## Review & editability

```json
"review": {
  "user_visible": true,
  "user_editable": true,
  "review_status": "pending_confirmation"
}
```

`review_status` is one of `unreviewed`, `pending_confirmation`, `confirmed`,
`rejected`.

## See also

- [Provenance & confidence](provenance.md)
- [Schema: claim.schema.json](https://ppx.dev/schemas/core/claim.schema.json)
