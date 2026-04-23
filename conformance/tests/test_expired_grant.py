"""L1: An access token whose grant is past expires_at is rejected."""
import os

import httpx
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_expired_grant_token_rejected(provider_url):
    """Provide PPX_EXPIRED_TOKEN via env; request MUST be rejected.

    Operators running conformance against a provider SHOULD mint a token bound
    to a grant whose `expires_at` is in the past, then set
    `PPX_EXPIRED_TOKEN` so this test can verify the provider rejects it.
    """
    token = os.environ.get("PPX_EXPIRED_TOKEN")
    if not token:
        pytest.skip("PPX_EXPIRED_TOKEN not set — provider MUST mint one for conformance")

    r = httpx.post(
        f"{provider_url}/v1/profile/effective",
        json={"context": {}},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    assert r.status_code in (401, 403), (
        f"expired-grant token MUST be rejected; got {r.status_code}"
    )
