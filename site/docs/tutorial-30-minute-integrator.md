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

> **Prerequisites: none.** Every step below runs against the public
> demonstration provider at **`https://ppx.dev/ppx`** — no signup, no
> Docker, no local stack. It is seeded with one subject and serves
> demonstration data only.
>
> Point `baseUrl` at your own provider when you have one; nothing in the
> code changes.

---

## 0. Register your app with the provider

A PPX provider needs to know what `client_id` your app uses so grant
requests can be tied to a real grantee. You'll need:

- A `client_id` (string)
- A `grantee_id` DID the provider associates with you
- An allowed redirect URL for the consent bounce-back

**On the public demo provider this is already done for you**: `fragrance-demo`
and `travel-demo` are registered, and the examples below use
`fragrance-demo`. Passing a `client_id` the provider does not know returns
`404 unknown_client` — grants are never issued to unregistered grantees.

!!! tip "The examples below use `fragrance-demo`"

    That way they run against a freshly seeded provider with no extra
    setup. Swap in your own `client_id` once you have registered one.
    Passing a `client_id` the provider does not know returns
    `404 unknown client_id: …`.

---

## 1. Install an SDK

The TypeScript client is published, and steps 2–6 use it:

```bash
npm i @blazing-customs/ppx-client
```

!!! note "Alpha, tracking a draft spec"

    Current version `0.1.0-alpha.1`. PPX is still a **draft**
    specification, so expect breaking changes between alphas.

!!! warning "The Python packages are not on PyPI yet"

    `pip install ppx-client` / `ppx-langchain` still 404. This affects
    **step 7 only** — steps 2–6 are TypeScript and run today. Until the
    Python packages ship, make the same calls directly against the HTTP
    binding; every SDK method is a thin wrapper over one documented HTTP
    request.

The examples are TypeScript; the Python shape is essentially identical.

---

## 2. Request a scoped grant

```ts
import { PpxClient, consentRedirectUrl, generatePkce } from "@blazing-customs/ppx-client";

const ppx = new PpxClient({ baseUrl: "https://ppx.dev/ppx" });

// PKCE is mandatory, and S256 is the only method — `plain` is refused. The
// verifier stays in this tab; only its SHA-256 goes to the provider now.
const pkce = await generatePkce();

const { grant_request_id, consent_url, request_token } = await ppx.requestGrant({
  client_id: "fragrance-demo",
  subject_id: "did:example:user-demo-0001",  // whose profile you're asking about
  purposes: ["recommendation", "explanation"],
  allowed_domains: ["fragrance"],
  allowed_namespaces: ["fragrance"],
  allowed_operations: ["read"],
  cross_domain_transfer: "deny",
  writeback_policy: "review_required",
  requested_duration_days: 30,
  code_challenge: pkce.challenge,
  code_challenge_method: "S256",
  // Matched EXACTLY against what you registered with the provider.
  redirect_uri: `${window.location.origin}/callback`,
});

// Stash the two secrets for the round trip. sessionStorage is tab-scoped and
// cleared when the tab closes; neither value may ever enter a URL.
sessionStorage.setItem(
  "ppx.pending",
  JSON.stringify({ grant_request_id, request_token, verifier: pkce.verifier }),
);
```

You now hold two different things, and the difference matters:

| | What it is | Where it may go |
|---|---|---|
| `grant_request_id` | a public handle | the consent URL, logs, anywhere |
| `request_token` | **the capability** | your app's memory only — never a URL |

`request_token` is returned exactly once and is not retrievable again. The
provider stores only its SHA-256.

The provider hasn't given you access to anything yet — the user still has to
approve.

---

## 3. Send the user to the provider's consent page

```ts
// Don't hardcode the consent host: the consent UI may live on a different
// origin from the API. `POST /v1/consent/request` already told you where
// to send the user.
window.location.href = consent_url;
```

There is no `return_to` parameter. The destination was pinned to your
registered `redirect_uri` when you created the request, so it cannot be
chosen — or rewritten — by whoever opens this URL.

The provider takes over: it authenticates the user, shows them exactly what
you asked for, lets them approve, narrow, or reject. When they're done, the
browser comes back to your registered callback with
`?grant_request_id=…&decision=approve`.

!!! warning "Treat the consent URL as public"
    It travels through referers, browser history, proxy and CDN logs,
    bookmarks and screenshots. That is safe here **because the id in it is
    inert** — on its own it exchanges for nothing. Never put the
    `request_token` or the PKCE verifier in a URL.

---

## 4. Mint a grant-scoped token

```ts
// In your /callback route
const search = new URLSearchParams(window.location.search);
const id = search.get("grant_request_id")!;
const decision = search.get("decision");

if (decision !== "approve") throw new Error("user declined");

// The id alone is NOT enough — that is the whole point. Bring the
// back-channel request_token and the PKCE verifier you stashed in step 2.
const pending = JSON.parse(sessionStorage.getItem("ppx.pending")!);
sessionStorage.removeItem("ppx.pending");   // one shot
if (pending.grant_request_id !== id) throw new Error("callback does not match a flow we started");

const token = await ppx.mintToken(
  id,
  pending.request_token,
  pending.verifier,
  "fragrance-demo",           // + a client_secret if you are a confidential client
);
//  → { access_token, token_type: "Bearer", expires_in: 3600, grant_id }

// Every failure here returns an identical `400 invalid_grant`. The provider
// deliberately will not tell you which check failed — a precise error would
// let someone holding a stray id work out what else they need.
```

Save `token.grant_id` to `localStorage` — you'll reuse it on return
visits to skip the consent flow.

```ts
localStorage.setItem("fragrance-demo.grant", token.grant_id);
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
import { PpxGrantRevokedError } from "@blazing-customs/ppx-client";

const cached = localStorage.getItem("fragrance-demo.grant");
if (cached) {
  try {
    const token = await ppx.refresh("fragrance-demo", cached);
    // you're back in business — fetch the profile as above
  } catch (err) {
    if (err instanceof PpxGrantRevokedError) {
      // user revoked at the provider; clear and prompt again
      localStorage.removeItem("fragrance-demo.grant");
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

ppx = PpxClient("https://ppx.dev/ppx")
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

ppx = PpxClient("https://ppx.dev/ppx")
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
- The user can revoke at any time. The next `refresh` returns `410 Gone`,
  and any read with an already-issued token starts returning `403` —
  revocation is immediate, not eventually-consistent.
- The user can approve **less** than you asked for. Always read what you
  actually got from the `grant` block in the response rather than assuming
  you were granted what you requested.
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
ppx-conformance --provider https://ppx.dev/ppx --level L1
```

(The conformance suite is not on PyPI — install it from the spec repo.)

Green means you're safe to link against any conforming provider, not
just the reference one. Run it in CI.

---

## 10. What's next

- **AG-UI consent streaming** — show live explanation text during the
  consent flow. See [`consent-and-trust.md`](consent-and-trust.md).
- **MCP binding** — expose the same PPX operations as MCP tools so any
  MCP-compatible agent can use them. See [`bindings/mcp.md`](bindings/mcp.md).
- **A2A binding** — call PPX from another agent. See
  [`bindings/a2a.md`](bindings/a2a.md).
- **Extension domains** — add a new namespace beyond `core` / `fragrance` /
  `travel`. See [`extensions/overview.md`](extensions/overview.md).

Total time to a working integration: ~30 minutes if you copy-paste,
maybe 60 if you write it yourself. Either way, you now have a
user-controlled, grant-scoped, auditable preference pipeline backing
your app — zero custom profile storage required.
