# `travel` namespace

Vocabulary for travel and environment preference claims.

## Keys (v0.1)

| Key | Value type | Description |
|---|---|---|
| `climate_heat_humidity_bias` | `float` | 0.0 = cold/dry; 1.0 = hot/humid. |
| `urbanism_preference` | `float` | 0.0 = rural; 1.0 = dense urban. |
| `pace_preference` | `float` | 0.0 = slow; 1.0 = packed. |
| `cultural_immersion_preference` | `float` | Depth of local-culture engagement. |
| `outdoor_activity_preference` | `float` | Outdoor/active vs indoor/sedentary. |
| `cuisine_openness` | `float` | Openness to unfamiliar cuisine. |
| `accommodation_style` | `string` | `hostel`, `boutique`, `business`, `luxury`, `homestay`, `rental`. |
| `group_size_preference` | `string` | `solo`, `pair`, `small_group`, `large_group`. |
| `trip_duration_preference_days` | `int` | Typical preferred trip length. |

## Privacy guidance

- `cross_domain_use`: **discouraged_without_review**.
- Travel keys MAY correlate with location inference and SHOULD NOT be freely
  shared cross-domain.
- Prefer core-namespace signals for cross-domain use.

## Schema

[Raw JSON](https://ppx.dev/schemas/extensions/travel.schema.json)
