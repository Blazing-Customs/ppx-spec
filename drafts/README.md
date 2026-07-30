# Drafts — written, but deliberately not published

Content that is finished enough to keep but would be wrong to put on the
public site yet, because a reader could not act on it.

| File | Blocked on |
| --- | --- |
| `30-minute-integrator.md` | Every step calls `@ppx/client` / `ppx-client`. Neither is on npm or PyPI, and the SDK source is not public, so a reader cannot follow it. Publish once the SDKs are released, or rewrite the steps against the HTTP binding. |

Move a file into `site/docs/` and add it to the `nav:` in `site/mkdocs.yml`
when its blocker clears.
