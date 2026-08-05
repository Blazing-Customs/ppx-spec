# Registry

The public directory of **providers** that implement PPX and **apps**
that integrate with it. A listing here signals that the party has
self-declared compliance with the spec; `verified` entries carry paid
certification and human review.

## Providers

Providers host PPX profiles and serve them via the spec's bindings
(HTTP, MCP, A2A, AG-UI). Click through for the provider's own docs
and terms.

{% for provider in registry_providers %}

### {{ provider.name }} {% if provider.tier == "verified" %}✅ verified{% endif %}

- **API:** `{{ provider.url }}`
- **Frontend:** `{{ provider.frontend_url or "—" }}`
- **Provider id:** `{{ provider.provider_id }}`
- **Docs:** {{ provider.docs_url or "—" }}
- **Source:** {{ provider.source_url or "—" }}
- **Description:** {{ provider.description }}

{% endfor %}

## Apps

Apps request scoped access to user profiles on some provider. Each app
declares the domains, purposes, and operations it needs.

{% for app in registry_apps %}

### {{ app.name }} — {{ app.category }}

- **Grantee:** `{{ app.grantee_id }}`
- **Domains:** {{ app.supported_domains | join(", ") }}
- **Purposes:** {{ app.supported_purposes | join(", ") }}
- **URL:** {{ app.url or "—" }}
- **Description:** {{ app.description }}

{% endfor %}

---

## How to get listed

See [`registry/README.md`](https://github.com/Blazing-Customs/ppx-spec/tree/main/registry)
in the spec repo. Submission is a JSON PR; CI runs the conformance suite
against provider URLs before merge.
