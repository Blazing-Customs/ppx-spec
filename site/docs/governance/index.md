---
title: Governance
description: How PPX namespaces are registered, how the spec is versioned, and how to propose a change.
---

# Governance

PPX is a draft-stage specification. Governance today is deliberately light:
one repository, public issues, and a written process for the three things
that need one — claiming a namespace, changing the spec, and shipping a
version.

## The documents

| Document | Answers |
| --- | --- |
| [Namespace registration](namespace-registration.md) | How do I claim an extension namespace such as `fragrance` or `travel`? |
| [Versioning](versioning.md) | What counts as a breaking change, and how are schemas versioned against the spec? |
| [Proposal template](proposal-template.md) | What does a substantive change proposal have to contain? |
| [Conformance levels](../conformance.md) | What do L1/L2/L3 mean, and what must a provider pass to claim each? |

## How a change happens

1. **Open an issue** describing the problem before writing a PR. Anything
   that touches the wire format, the consent model, or a schema starts as
   a discussion.
2. **Write a proposal** using the [proposal template](proposal-template.md)
   if the change is substantive — a new namespace, a new binding target, or
   anything breaking.
3. **Open a PR** against `main`. Schema changes must keep the validation
   workflow green and the conformance suite passing.
4. **Version it** per the [versioning policy](versioning.md) and record it
   in the [changelog](../changelog.md).

## Who decides, for now

PPX is maintained by its original authors while it is pre-1.0. The intent
stated in the spec is to move to a neutral working group as adoption grows;
until then, decisions are made in the open on the issue tracker and every
resolution is written down in one of the documents above.

See [Community](../community.md) for where discussion happens.
