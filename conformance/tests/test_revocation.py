"""L1: Revoked grants must stop authorizing access within 60 seconds."""
import os
import time

import httpx
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_revoked_grant_denies_within_60s(provider_url):
    """Operator provides a revocable grant + its access token via env:

    - PPX_REVOCABLE_GRANT_ID: the grant to revoke
    - PPX_REVOCABLE_TOKEN: a bearer token bound to that grant
    - PPX_REVOKE_TOKEN: a privileged token authorized to call /v1/consent/revoke
    """
    grant_id = os.environ.get("PPX_REVOCABLE_GRANT_ID")
    token = os.environ.get("PPX_REVOCABLE_TOKEN")
    revoke_token = os.environ.get("PPX_REVOKE_TOKEN")

    if not (grant_id and token and revoke_token):
        pytest.skip(
            "PPX_REVOCABLE_GRANT_ID / PPX_REVOCABLE_TOKEN / PPX_REVOKE_TOKEN "
            "not set — operator MUST provide these for conformance"
        )

    # Baseline: token works.
    baseline = httpx.post(
        f"{provider_url}/v1/profile/effective",
        json={"context": {}},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    assert baseline.status_code == 200, f"baseline access should succeed; got {baseline.status_code}"

    # Revoke.
    rev = httpx.post(
        f"{provider_url}/v1/consent/revoke",
        json={"grant_id": grant_id},
        headers={"Authorization": f"Bearer {revoke_token}"},
        timeout=10.0,
    )
    assert rev.status_code in (200, 204), f"revoke call failed: {rev.status_code}"

    deadline = time.time() + 60.0
    while time.time() < deadline:
        r = httpx.post(
            f"{provider_url}/v1/profile/effective",
            json={"context": {}},
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        if r.status_code in (401, 403):
            return
        time.sleep(2.0)

    pytest.fail("revoked grant still authorized access after 60s")
