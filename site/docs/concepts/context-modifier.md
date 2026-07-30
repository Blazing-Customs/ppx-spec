# Context modifier

A **Context Modifier** alters how claims SHOULD be interpreted under specific
conditions.

## Why

Preferences are rarely context-free. Someone who likes heavy woody fragrances
*in general* may prefer fresh airy scents *in hot/humid weather*. Rather
than storing a separate claim for every `(preference, context)` combination,
PPX expresses this as a modifier that adjusts the base claim under matching
conditions.

## Shape

```json
{%
  include "../../../examples/context-modifier-climate.json"
%}
```

## Core context dimensions (v0.1)

- `climate`, `season`, `time_of_day`, `occasion`, `social_context`,
  `stress_level`, `budget_sensitivity`, `time_horizon`.

Extensions MAY add domain-specific context dimensions.

## Effect types

| `effect_type` | Meaning |
|---|---|
| `weight_adjustment` | Multiplicatively raises/lowers claim weights. |
| `override` | Replaces a claim value under the condition. |
| `veto` | Removes a claim from consideration. |
| `suggest` | Surface a claim only when condition holds. |

## Resolution order

When a client calls `get_effective_profile` with a context, the provider:

1. Loads the user's claims (subject to grant scope).
2. Finds all modifiers whose `condition` matches the supplied context.
3. Applies their `effect` to the resolved claim set.
4. Returns the effective profile.

The order of modifier application SHOULD be stable (alphabetical by
`modifier_id`) so that results are reproducible.

## See also

- [Schema: context-modifier.schema.json](https://ppx.dev/schemas/core/context-modifier.schema.json)
