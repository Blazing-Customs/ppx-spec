# Schemas

All PPX schemas are published as [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema)
documents. They are the **authoritative source** for structural constraints.

## Core schemas

| Schema | Raw | Description |
|---|---|---|
| `profile` | [JSON][p-json] | User-scoped collection of claims, modifiers, grants. |
| `claim` | [JSON][c-json] | A single machine-readable preference statement. |
| `context-modifier` | [JSON][cm-json] | Alters claim interpretation under conditions. |
| `consent-grant` | [JSON][g-json] | Scoped authorization for a grantee. |
| `evidence-ref` | [JSON][e-json] | Pointer to supporting data for a claim. |
| `discovery-card` | [JSON][d-json] | Provider advertisement at `/.well-known/ppx-card.json`. |
| `extension-descriptor` | [JSON][ed-json] | Domain vocabulary descriptor. |
| `derived-view` | [JSON][dv-json] | Task-scoped projection over one or more profiles. |

[p-json]: https://ppx.dev/schemas/core/profile.schema.json
[c-json]: https://ppx.dev/schemas/core/claim.schema.json
[cm-json]: https://ppx.dev/schemas/core/context-modifier.schema.json
[g-json]: https://ppx.dev/schemas/core/consent-grant.schema.json
[e-json]: https://ppx.dev/schemas/core/evidence-ref.schema.json
[d-json]: https://ppx.dev/schemas/core/discovery-card.schema.json
[ed-json]: https://ppx.dev/schemas/core/extension-descriptor.schema.json
[dv-json]: https://ppx.dev/schemas/core/derived-view.schema.json

## Extension schemas

| Namespace | Raw |
|---|---|
| `core` | [JSON](https://ppx.dev/schemas/extensions/core.schema.json) |
| `fragrance` | [JSON](https://ppx.dev/schemas/extensions/fragrance.schema.json) |
| `travel` | [JSON](https://ppx.dev/schemas/extensions/travel.schema.json) |

## Validating against the schemas

```bash
pip install jsonschema
python3 - <<'PY'
import json, urllib.request
from jsonschema import Draft202012Validator
url = "https://raw.githubusercontent.com/Blazing-Customs/ppx-spec/main/schemas/core/claim.schema.json"
schema = json.loads(urllib.request.urlopen(url).read())
instance = {
    "claim_id": "ppx:claim:example",
    "type": "preference",
    "namespace": "core",
    "key": "novelty_tolerance",
    "value": 0.62,
    "confidence": 0.78,
    "source": { "kind": "user_stated" }
}
errors = list(Draft202012Validator(schema).iter_errors(instance))
print("valid" if not errors else errors)
PY
```

## Stability

Schema shape in `0.x` is **not** stable. See the
[versioning policy](../governance/versioning.md) for the rules that apply
once `1.0` ships.
