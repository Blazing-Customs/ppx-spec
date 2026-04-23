# `fragrance` namespace

Vocabulary for fragrance and scent preference claims. Built as the first
domain extension to drive the canonical fragrance → travel cross-domain
demo.

## Keys (v0.1)

| Key | Value type | Description |
|---|---|---|
| `family_preference` | `map<string,float>` | Relative affinity for fragrance families (`woody`, `citrus`, `floral`, etc.). |
| `intensity_preference` | `float` | Preferred overall scent intensity at skin. |
| `projection_tolerance` | `float` | Tolerance for scent projecting beyond wearer. |
| `longevity_preference` | `float` | Preferred on-skin duration. |
| `sweetness_preference` | `float` | Preference for sweet/gourmand facets. |
| `freshness_preference` | `float` | Preference for airy/aquatic/citrus-fresh profiles. |
| `occasion_bias` | `map<string,float>` | Map of occasion → family-skew affinity. |
| `note_aversions` | `string_list` | Explicitly disliked notes. |

## Privacy guidance

- `cross_domain_use`: **discouraged_without_review**.
- Raw fragrance-family data is domain-specific and SHOULD NOT be reused
  cross-domain.
- Transferable signals SHOULD be mapped into the `core` namespace under
  grant review.

## Schema

[Raw JSON](https://github.com/Blazing-Customs/ppx-spec/blob/main/schemas/extensions/fragrance.schema.json)
