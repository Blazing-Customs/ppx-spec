# Contributing to PPX

PPX is a **draft specification at v0.1.0-draft**. It is pre-standardization
and pre-stable: breaking changes are expected before 1.0, and the governance
model is deliberately lightweight while the spec is this young.

Review is worth more to us right now than code. If you have implemented
something adjacent — an agent memory layer, a preference store, a consent
UX — the most useful thing you can do is tell us where PPX would have got in
your way.

## Ways to contribute, roughly by value

1. **Review the consent model.** Section 6 of [`SPEC.md`](SPEC.md) is the part
   most likely to be wrong in a way that matters. Cross-domain transfer,
   revocation semantics, and write-back review are the sharp edges.
2. **Try a binding against a real client.** The [bindings](bindings/) claim
   PPX maps cleanly onto MCP, A2A, AG-UI, A2UI and HTTP. If one of those
   mappings breaks against a real implementation, that is a spec bug.
3. **Propose a domain namespace.** `fragrance` and `travel` exist to prove the
   extension mechanism works, not because those domains are special.
4. **Fix the docs.** Anything unclear, wrong, or unfollowable.

## Before you open a pull request

**Open an issue first** for anything non-trivial. A rejected PR that took you
an afternoon is a worse outcome for both of us than a five-minute issue.

Substantive changes — a new namespace, a new binding target, anything
breaking — need a written proposal using
[`governance/PROPOSAL-TEMPLATE.md`](governance/PROPOSAL-TEMPLATE.md).

Typo fixes, broken links, and clarifications need no ceremony. Just open the
PR.

## Working on the repo

```bash
git clone https://github.com/Blazing-Customs/ppx-spec
cd ppx-spec
```

Validate the schemas (the `validate-schemas` workflow runs this on every PR):

```bash
pip install jsonschema referencing
python -c "
import glob, json
from jsonschema import Draft202012Validator
for f in glob.glob('schemas/**/*.schema.json', recursive=True):
    Draft202012Validator.check_schema(json.load(open(f)))
    print('ok', f)
"
```

Run the conformance suite. The schema-level tests run offline; the rest need
a live provider:

```bash
pip install -e conformance
pytest conformance                      # offline subset
PPX_PROVIDER_URL=http://localhost:7700 pytest conformance   # full suite
```

Build the docs site:

```bash
pip install -r site/requirements.txt
cd site && mkdocs serve
```

`mkdocs build --strict` must be clean. Note that pages built by including a
file from the repo root (`SPEC.md`, `bindings/*`, `governance/*`) have their
links repaired by `site/hooks/repo_links.py` — if you add a new repo-root
document that other documents link to, add it to the map in that hook.

## What a good change looks like

- **Schema changes are additive** wherever possible. A change that invalidates
  an existing valid payload is breaking, and needs the versioning policy
  applied — see [`governance/VERSIONING.md`](governance/VERSIONING.md).
- **Normative language is deliberate.** MUST / SHOULD / MAY are used in the
  RFC 2119 sense. Do not upgrade a SHOULD to a MUST without saying why.
- **Claims are checkable.** If you state that something works, say how you
  verified it. This applies to spec prose as much as to code.
- **One concern per PR.**

## Licensing

By contributing you agree that your contribution is licensed under the same
terms as the material it touches:

- Normative prose under [CC BY 4.0](LICENSE-SPEC)
- Schemas, examples, and code under [Apache 2.0](LICENSE-SCHEMAS)

## Governance and decisions

Decisions are made in the open on the issue tracker and written down in
[`governance/`](governance/). While PPX is pre-1.0 the original authors are
the maintainers; the stated intent is to move to a neutral working group as
adoption grows. If that matters to your adoption decision, say so in an
issue — it is useful signal.

## Reporting a security issue

Do not open a public issue. See [SECURITY.md](SECURITY.md).
