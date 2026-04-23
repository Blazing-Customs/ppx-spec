"""L1: A grant with cross_domain_transfer=deny rejects cross-domain requests."""
import os

import httpx
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_cross_domain_request_denied_when_policy_deny(provider_url):
    """Operator provides PPX_DENY_CROSSDOMAIN_TOKEN bound to a grant whose
    `allowed_domains=['fragrance']` and `cross_domain_transfer=deny`. Asking
    the provider to use fragrance data in a travel context MUST be rejected.
    """
    token = os.environ.get("PPX_DENY_CROSSDOMAIN_TOKEN")
    if not token:
        pytest.skip("PPX_DENY_CROSSDOMAIN_TOKEN not set — skipping")

    r = httpx.post(
        f"{provider_url}/v1/profile/effective",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "context": {"climate": "hot_humid"},
            "requested_domain": "travel"
        },
        timeout=10.0,
    )
    assert r.status_code in (403, 409), (
        f"cross-domain request under deny policy MUST be rejected; "
        f"got {r.status_code}: {r.text[:200]}"
    )
