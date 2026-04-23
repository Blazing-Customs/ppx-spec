# Binding: PPX over AG-UI

**Target:** AG-UI v0.1.0+.

This document is normative for providers claiming the `ag_ui_supported` UI
capability in their discovery card.

## Overview

AG-UI carries **live** agent↔app interactions. PPX user-facing flows — consent
prompts, claim review, explanation surfaces, profile diffs, audit views —
SHOULD use AG-UI event streams so that frontends can react incrementally and
maintain shared state with the provider.

## Recommended event types

| PPX flow | AG-UI event type(s) |
|---|---|
| Initial profile render | `STATE_SNAPSHOT` |
| Claim added / confidence changed / expires_at updated | `STATE_DELTA` |
| Consent prompt ("approve grant for fragrance agent?") | `INTERRUPT` |
| Explanation text streamed to user | `TEXT_MESSAGE_START` → `TEXT_MESSAGE_CONTENT` → `TEXT_MESSAGE_END` |
| User approves / rejects / revokes via UI | `TOOL_CALL_START` → `TOOL_CALL_ARGS` → `TOOL_CALL_RESULT` |
| End of a review session | `RUN_FINISHED` |

## State snapshot shape

The initial `STATE_SNAPSHOT` payload for a PPX review session SHOULD contain
a projection suitable for client rendering:

```json
{
  "profile_id": "ppx:profile:...",
  "claims": [ /* subset of Claim objects, user-visible only */ ],
  "pending_reviews": [ /* claims with review_status=pending_confirmation */ ],
  "active_grants": [ /* ConsentGrant objects, status=active */ ]
}
```

Subsequent `STATE_DELTA` events MUST be JSON Patch (RFC 6902) operations
relative to the last snapshot.

## Consent prompt pattern

A consent request is surfaced as an `INTERRUPT` event whose `data` block
contains the proposed ConsentGrant in draft form. The UI renders it; the user
approves, edits, or rejects; the decision is returned to the provider via a
`TOOL_CALL_*` sequence that eventually materializes the grant.

```json
{
  "type": "INTERRUPT",
  "data": {
    "kind": "ppx.consent_request",
    "grant_draft": { /* proposed ConsentGrant */ },
    "actions": ["approve", "edit", "reject"]
  }
}
```

## Auth

AG-UI runs on top of the provider's normal OAuth2.1 session; no separate PPX
auth is introduced by this binding.

## Non-goals

- This binding does not define the rendered components themselves — see
  [`a2ui.md`](a2ui.md).
- This binding does not specify offline or long-lived subscription
  semantics.
