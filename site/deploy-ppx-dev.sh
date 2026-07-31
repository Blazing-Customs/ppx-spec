#!/bin/bash
# Build the docs site and publish it to https://ppx.dev/.
#
# READ THIS BEFORE CHANGING THE RSYNC FLAGS.
#
# ppx.dev is not only a docs site. The same docroot serves:
#
#   /schemas/     the normative JSON Schemas. These URLs are the schema $id
#                 values that validators resolve. Breaking them breaks every
#                 downstream consumer, silently.
#   /examples/    example documents referenced by the docs
#   /ppx/         the live PPX provider (conformance 30/30)
#   /apps/        the live demo applications + their hub (static exports)
#   /.well-known/ discovery card and JWKS
#
# `mkdocs build` emits its own copies of /schemas/ and /examples/ (a hook
# copies them out of the repo), and those ARE the source of truth - verified
# byte-identical to what is live. So rsync may overwrite them. What it must
# NEVER do is DELETE the paths mkdocs knows nothing about, which is what
# `--delete` would do without the excludes below.
#
# .htaccess is excluded at every level: the root one carries the CORS headers
# and the application/schema+json content type that make the schema $ids
# usable cross-origin, and it is maintained on the server, not here.

set -euo pipefail

HOST="${PPX_DEPLOY_HOST:-findthatstream}"
DEST="${PPX_DEPLOY_PATH:-~/ppx.dev/}"
HERE="$(cd "$(dirname "$0")" && pwd)"

cd "$HERE"

echo "==> building"
mkdocs build --strict

echo "==> verifying the built schemas match what is already live"
cd site
fail=0
for f in $(find schemas examples -type f | sort); do
  live=$(curl -sS -f "https://ppx.dev/$f" 2>/dev/null | sha256sum | cut -d' ' -f1)
  built=$(sha256sum "$f" | cut -d' ' -f1)
  if [ -n "$live" ] && [ "$live" != "$built" ]; then
    echo "    CHANGED: $f"
    fail=$((fail + 1))
  fi
done
if [ "$fail" -gt 0 ]; then
  echo "    ^ $fail schema/example file(s) differ from production."
  echo "      That may be intentional (a real schema change) - but confirm it is,"
  echo "      because these URLs are published \$ids. Re-run with PPX_ALLOW_SCHEMA_CHANGE=1."
  [ "${PPX_ALLOW_SCHEMA_CHANGE:-0}" = "1" ] || exit 1
fi

echo "==> dry run"
rsync -rn --delete --itemize-changes \
  --exclude='.htaccess*' \
  --exclude='/ppx' \
  --exclude='/apps' \
  --exclude='/.well-known' \
  --exclude='/cgi-bin' \
  --exclude='*.bak-*' \
  ./ "$HOST:$DEST" | grep '^\*deleting' || echo "    (no deletions)"

echo "==> deploying"
rsync -rz --delete \
  --exclude='.htaccess*' \
  --exclude='/ppx' \
  --exclude='/apps' \
  --exclude='/.well-known' \
  --exclude='/cgi-bin' \
  --exclude='*.bak-*' \
  ./ "$HOST:$DEST"

echo "==> post-deploy checks"
for u in / /spec/ /tutorial-30-minute-integrator/ \
         /schemas/core/profile.schema.json \
         /examples/profile-basic.json \
         /ppx/.well-known/ppx-card.json; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "https://ppx.dev$u")
  printf '    %-46s %s\n' "$u" "$code"
  [ "$code" = "200" ] || { echo "    ^ FAILED"; exit 1; }
done

echo "==> done: https://ppx.dev/"
