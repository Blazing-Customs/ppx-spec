# `core` namespace

The core namespace intentionally stays generic and cross-cutting. All core
keys take values in `[0.0, 1.0]` with `units = normalized_0_1`.

## Keys (v0.1)

| Key | Description |
|---|---|
| `novelty_tolerance` | 0.0 = strong familiarity preference; 1.0 = strong novelty preference. |
| `risk_tolerance` | General comfort with uncertainty and potential downside. Not a financial risk score. |
| `regret_sensitivity` | Sensitivity to post-choice regret. High values SHOULD push systems toward safer, reversible options. |
| `sensory_intensity_preference` | Preferred sensory intensity across modalities. |
| `social_energy_preference` | 0.0 = solitary-leaning; 1.0 = gregarious-leaning. |
| `decision_speed_preference` | 0.0 = deliberative; 1.0 = quick. |
| `ambiguity_tolerance` | Comfort with under-specified or open-ended situations. |
| `budget_sensitivity` | Price-awareness; NOT a discretionary-income measure. |
| `explanation_depth_preference` | 0.0 = concise; 1.0 = thorough. |
| `conversation_depth_preference` | 0.0 = breadth-oriented; 1.0 = depth-oriented. |

## Privacy guidance

- `cross_domain_use`: **recommended** — core keys are designed to be safely
  transferable across domains under a grant.
- Core keys MUST NOT carry identifying information.

## Schema

[Raw JSON](https://ppx.dev/schemas/extensions/core.schema.json)
