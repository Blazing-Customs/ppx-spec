# Drafts — written, but deliberately not published

Content that is finished enough to keep but would be wrong to put on the
public site yet, because a reader could not act on it.

_Nothing is currently blocked._

| File | Blocked on |
| --- | --- |
| — | — |

**`30-minute-integrator.md` shipped on 2026-07-30** and now lives at
`site/docs/tutorial-30-minute-integrator.md`. Its blocker — no public
provider implementing the consent-grant flow — was cleared by adding
`consent/request`, `approve`, `reject`, `token`, `refresh`, `grants` and a
browser consent screen to the PHP provider at `https://ppx.dev/ppx`. The
tutorial now has **no prerequisites at all**: every step runs against that
public endpoint with no signup and no local stack.

Move a file into `site/docs/` and add it to the `nav:` in `site/mkdocs.yml`
when its blocker clears.

## Verification log

`30-minute-integrator.md` — 2026-07-30, run against a live reference
provider (`docker compose up postgres redis backend`) using the published
`@blazing-customs/ppx-client@0.1.0-alpha.1` installed from npm:

| Step | Result |
| --- | --- |
| 2 · `requestGrant` | pass — returns a pending request id |
| 3 · `consentRedirectUrl` | pass — URL built, `return_to` percent-encoded |
| 3b · user approval | pass — `POST /v1/consent/approve` → 200 |
| 4 · `mintToken` | pass — Bearer, `expires_in` 3600 |
| 5 · `effectiveProfile` | pass — 5 fragrance claims, 1 context modifier applied |
| 6 · `refresh` | pass — re-mints with no user interaction |
| 6b · revoked grant | pass — raises `PpxGrantRevokedError`, as documented |
| 7 · LangChain / Google ADK | **not executed** — Python SDKs not on PyPI |

Two documentation fixes came out of that run:

1. The runnable examples now use the seeded `fragrance-demo` client.
   Copy-pasting the previous `scent-advisor` returned
   `404 unknown client_id` on a freshly seeded provider — step 0 explained
   registration, but the code did not run as written.
2. Step 1 no longer claims no SDK is published; it now installs the
   TypeScript client and scopes the "not published" warning to step 7.

## Spec gaps found by running two implementations against one client

Both surfaced on 2026-07-30 when the published `ppx-client` was pointed at
the independent PHP provider. Neither is a client-only issue; both are
places the specification is thinner than it looks.

1. **JWKS location is discovered, not fixed — but that is easy to miss.**
   `SPEC.md` pins only `/.well-known/ppx-card.json`; the grant-signing key
   set is wherever `signing.grant_jwks_uri` in the card points. The client
   had hardcoded the Python reference provider's
   `/.well-known/ppx-grant-jwks.json` and 404'd against the PHP provider,
   which publishes `/.well-known/jwks.json`. The client now follows the
   card. Worth stating explicitly in the binding.

2. **The `/v1/profile/effective` response body is not specified.**
   `profile.schema.json` requires `profile_id`, but that schema describes a
   stored Profile *document*; neither `SPEC.md` nor `bindings/http.md`
   defines what this endpoint returns. The Python provider returns
   `profile_id`; the PHP provider returns `subject_id` + `provider_id` +
   `generated_at`. Both pass conformance, because the suite does not assert
   the shape. **This needs a normative decision and a conformance test.**
