# Examples

All examples in this section are valid instances of their declared schemas.
Every example here is validated in CI via the
[conformance suite](https://github.com/Blazing-Customs/ppx-spec/tree/main/conformance).

## A basic profile

```json
{%
  include "../../../examples/profile-basic.json"
%}
```

## A fragrance grant

Domain-scoped, 30-day, read + propose_update.

```json
{%
  include "../../../examples/grant-fragrance.json"
%}
```

## A travel grant with cross-domain review

Core-only, 7-day, read-only, `allow_with_review` cross-domain. This is the
canonical cross-domain consent pattern.

```json
{%
  include "../../../examples/grant-travel.json"
%}
```

## A derived compatibility view

```json
{%
  include "../../../examples/derived-view-dating.json"
%}
```

Note: the derived view exposes **signals and explanations**, not raw claim
values.

## A discovery card

```json
{%
  include "../../../examples/discovery-card.json"
%}
```

## A climate context modifier

```json
{%
  include "../../../examples/context-modifier-climate.json"
%}
```
