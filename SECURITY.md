# Security policy

## Scope

This repository holds a **specification**, its JSON Schemas, and a
conformance test suite. It is not a deployed service. Two different kinds of
security report are in scope:

1. **Specification weaknesses** — a flaw in the consent, grant, revocation, or
   provenance model that would let a conforming implementation leak or misuse
   profile data even when it follows the spec correctly. These are the ones we
   most want to hear about.
2. **Defects in this repository's code** — the conformance suite, the schemas,
   or the docs build.

Vulnerabilities in the reference provider belong in
[`ppx-provider`](https://github.com/Blazing-Customs/ppx-provider).

## Reporting

Use GitHub's private vulnerability reporting on this repository
(**Security → Report a vulnerability**). Please do not open a public issue
for a spec-level weakness before we have discussed it.

Include what a conforming implementation would do, and what an attacker gets
out of it. A concrete sequence of grants and requests is far more useful than
a description.

## What to expect

PPX is a draft specification maintained by a small team. We will acknowledge
your report and tell you whether we consider it in scope. We are not offering
a bounty and cannot commit to a fixed remediation window.

If a report changes normative behaviour, the resulting change goes through the
[versioning policy](governance/VERSIONING.md) like any other breaking change,
and the changelog will credit you unless you prefer otherwise.

## Supported versions

`v0.1.0-draft` is the only version. It is a draft and carries no stability or
security guarantee. Do not put real user data behind a PPX implementation
until the spec reaches 1.0 and your implementation has had its own review.
