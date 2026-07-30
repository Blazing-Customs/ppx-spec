<!-- Typo and broken-link fixes: delete all of this, describe the fix in one line, open it. -->

## What this changes

<!-- One paragraph. Link the issue this came out of. -->

## Why

<!-- What is wrong today. If this came from an implementation that hit the problem, say which. -->

## Normative impact

- [ ] Editorial only — no change to what an implementation must do
- [ ] Additive — existing valid payloads stay valid, existing providers stay conformant
- [ ] **Breaking** — invalidates existing payloads or changes required behaviour

If breaking, link the proposal (`governance/PROPOSAL-TEMPLATE.md`) and say what
the versioning policy calls for.

## Checks

- [ ] Schemas still validate against Draft 2020-12
- [ ] `pytest conformance` passes (offline subset), and the full suite passes against a provider if this touches wire behaviour
- [ ] `mkdocs build --strict` is clean
- [ ] `CHANGELOG.md` updated if this is user-visible
