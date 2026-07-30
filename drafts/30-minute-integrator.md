# Build a PPX-native app in 30 minutes

This tutorial walks through making an app PPX-aware from zero. By the end
you'll have:

1. Requested a scoped grant from a PPX provider,
2. Bounced the user through the provider's consent page,
3. Minted a grant-scoped token,
4. Read the user's preferences under that scope,
5. Re-minted the token on return visits without re-prompting,
6. Handed the same grant to an AI agent via LangChain or Google ADK so
   the agent can reason about the user's preferences.

Total code: ~80 lines of TypeScript (or Python) + ~30 lines of agent glue.

> **Prerequisites.** A running PPX provider at some URL — the reference
> provider ([Blazing-Customs/ppx-provider](https://github.com/Blazing-Customs/ppx-provider))
> spins up on `docker compose up` and exposes everything you need. The
> examples below assume `http://localhost:7700`; swap in your provider.

---

## 0. Register your app with the provider

A PPX provider needs to know what `client_id` your app uses so grant
requests can be tied to a real grantee. In the reference provider this
is rows in the `api_clients` table; other providers expose a
self-service form. You'll need:

- A `client_id` (string, e.g. `scent-advisor`)
- A `grantee_id` DID the provider associates with you (e.g. `did:example:agent:scent-advisor`)
- An allowed redirect URL for the consent bounce-back

If you're on the reference provider, `scripts/seed_dev_data.py` creates
`fragrance-demo` and `travel-demo` out of the box — use those or add
your own.

---

## 1. Install an SDK

!!! warning "There is no SDK to install yet"

    PPX is a draft specification. **No PPX package has been published to PyPI
    or npm, and the SDK source is not yet public.** `pip install ppx-client`
    and `npm i @ppx/client` both fail today. Those names are reserved intent.

    The code below shows the **shape** of a PPX integration using the planned
    client API. It is not runnable today. Until the SDKs are released, make
    the same calls directly against the HTTP binding — every SDK method here
    is a thin wrapper over one documented HTTP request.

The examples are TypeScript; the Python shape is essentially identical.

---

## 2. Request a scoped grant

```ts
import { PpxClient, consentRedirectUrl } from "@ppx/client";

const ppx = new PpxClient({ baseUrl: "http://localhost:7700" });

const { grant_request_id } = await ppx.requestGrant({
  client_id: "scent-advisor",
  subject_id: "did:example:user-demo-0001",  // whose profile you're asking about
  purposes: ["recommendation", "explanation"],
  allowed_domains: ["fragrance"],
  allowed_namespaces: ["fragrance"],
  allowed_operations: ["read"],
  cross_domain_transfer: "deny",
  writeback_policy: "review_required",
  requested_duration_days: 30,
});
```

The provider hasn't given you anything yet — just a request ID the user
has to approve.

---

## 3. Send the user to the provider's consent page

```ts
const returnTo = `${window.location.origin}/callback`;
window.location.href = consentRedirectUrl(
  "http://localhost:7703",   // provider frontend, not API
  grant_request_id,
  returnTo,
);
```

The provider takes over: it authenticates the user (Keycloak on the
reference provider), shows them exactly what you asked for, lets them
approve, narrow, or reject. When they're done, the browser comes back
to `returnTo` with `?grant_request_id=…&decision=approve`.

---

## 4. Mint a grant-scoped token

```ts
// In your /callback route
const search = new URLSearchParams(window.location.search);
const id = search.get("grant_request_id")!;
const decision = search.get("decision");

if (decision !== "approve") throw new Error("user declined");

const token = await ppx.mintToken(id);
//  → { access_token, token_type: "Bearer", expires_in: 3600, grant_id }
```

Save `token.grant_id` to `localStorage` — you'll reuse it on return
visits to skip the consent flow.

```ts
localStorage.setItem("scent-advisor.grant", token.grant_id);
```

---

## 5. Read the user's scoped preferences

```ts
const profile = await ppx.effectiveProfile(
  {
    context: { climate: "hot_humid", occasion: "date_night" },
    requested_namespaces: ["fragrance"],
  },
  token.access_token,
);

for (const claim of profile.claims) {
  console.log(`${claim.namespace}.${claim.key}`, claim.value, claim.confidence);
}
```

The provider applies any relevant context modifiers (e.g. climate-bias
tweaks) before returning. Claims you didn't ask for — or that fall
outside the grant — are silently omitted.

---

## 6. Return visits skip the consent flow

On the next page load, check localStorage and re-mint directly:

```ts
import { PpxGrantRevokedError } from "@ppx/client";

const cached = localStorage.getItem("scent-advisor.grant");
if (cached) {
  try {
    const token = await ppx.refresh("scent-advisor", cached);
    // you're back in business — fetch the profile as above
  } catch (err) {
    if (err instanceof PpxGrantRevokedError) {
      // user revoked at the provider; clear and prompt again
      localStorage.removeItem("scent-advisor.grant");
      // → fall back to step 2
    } else throw err;
  }
}
```

This mirrors OAuth 2.1 refresh semantics: the grant is the long-lived
authorization artifact, the access token is short-lived and derived.

---

## 7. Let an AI agent use the grant

Two integrations covered — pick whichever matches your stack.

### LangChain

```python
from ppx_client import PpxClient
from ppx_langchain import ppx_preference_tool
from langchain_openai import ChatOpenAI

ppx = PpxClient("http://localhost:7700")
tool = ppx_preference_tool(ppx, grant_token=my_grant_token)

llm = ChatOpenAI(model="gpt-4o-mini").bind_tools([tool])
response = llm.invoke(
    "Suggest a fragrance for tonight. Use lookup_user_preference to check the user's profile."
)
```

The LLM calls `lookup_user_preference("fragrance")`; the call is routed
through the same grant your browser code uses. Every read is scoped.

### Google ADK

```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from ppx_client import PpxClient
from ppx_google_adk import build_preference_tool, fetch_preference_context

ppx = PpxClient("http://localhost:7700")
preferences = fetch_preference_context(
    ppx, grant_token=my_grant_token,
    requested_namespaces=["core", "fragrance"],
    context={"climate": "hot_humid"},
)
lookup = build_preference_tool(ppx, grant_token=my_grant_token)

agent = LlmAgent(
    name="scent_advisor",
    model="gemini-2.0-flash",
    instruction=(
        "Recommend fragrances. Use the user's preferences below and the "
        "lookup_user_preference tool if you need more detail.\n\n" + preferences
    ),
    tools=[FunctionTool(lookup)],
)
```

You can mix both patterns — seed the agent with baseline context at
session start, then let it refine on demand via the tool.

---

## 8. Where the boundaries are

- Your app **never** sees claims outside the grant. Keys you didn't list
  are silently redacted, not rejected.
- The user can revoke at any time in the provider's connected-apps page.
  The next call you make (refresh or profile read) returns `410 Gone`.
- Cross-domain transfer (using data derived in one domain — say fragrance —
  in another, say travel) **requires explicit `allow_with_review`** in
  the grant. Anything else is denied at the grant engine.
- Writeback (`propose_update`) is deny-by-default. Under `review_required`,
  proposed claim updates wait for the user's approval before they take effect.

---

## 9. Verify you're spec-compliant

Every conforming client should pass the same round-trip tests a
conforming provider does. Use the conformance suite:

```bash
git clone https://github.com/Blazing-Customs/ppx-spec
pip install -e ppx-spec/conformance
ppx-conformance --provider http://localhost:7700 --level L1
```

(Also not on PyPI yet — install it from the spec repo.)

Green means you're safe to link against any conforming provider, not
just the reference one. Run it in CI.

---

## 10. What's next

- **AG-UI consent streaming** — show live explanation text during the
  consent flow. See [`consent-and-trust.md`](../consent-and-trust.md).
- **MCP binding** — expose the same PPX operations as MCP tools so any
  MCP-compatible agent can use them. See [`bindings/mcp.md`](../bindings/mcp.md).
- **A2A binding** — call PPX from another agent. See
  [`bindings/a2a.md`](../bindings/a2a.md).
- **Extension domains** — add a new namespace beyond `core` / `fragrance` /
  `travel`. See [`extensions/overview.md`](../extensions/overview.md).

Total time to a working integration: ~30 minutes if you copy-paste,
maybe 60 if you write it yourself. Either way, you now have a
user-controlled, grant-scoped, auditable preference pipeline backing
your app — zero custom profile storage required.
