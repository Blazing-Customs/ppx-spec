# Drafts — written, but deliberately not published

Content that is finished enough to keep but would be wrong to put on the
public site yet, because a reader could not act on it.

| File | Blocked on |
| --- | --- |
| `30-minute-integrator.md` | **One blocker left: `ppx-provider` is private.** The tutorial's prerequisite is a running provider via `docker compose up` from that repo, which a stranger cannot clone. Move to `site/docs/` once `ppx-provider` is public, or once a hosted demo provider exists that readers can point at. |

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
