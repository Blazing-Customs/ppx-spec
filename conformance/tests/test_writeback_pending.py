"""L3: propose_updates with writeback_policy=review_required creates a pending review."""
import pytest


@pytest.mark.level3
@pytest.mark.requires_provider
def test_propose_update_stays_pending(provider_client):
    """When the active grant's writeback_policy is review_required,
    propose_updates MUST NOT directly mutate the claim; it MUST create a
    pending review. The response SHOULD indicate `writeback: proposal_created`.
    """
    payload = {
        "claims": [
            {
                "namespace": "fragrance",
                "key": "projection_tolerance",
                "value": 0.55,
                "value_type": "float",
                "units": "normalized_0_1",
                "source": {
                    "kind": "observed",
                    "origin": "conformance_test"
                }
            }
        ]
    }
    r = provider_client.post("/v1/profile/propose-updates", json=payload)
    assert r.status_code in (200, 202), f"expected 200/202, got {r.status_code}: {r.text[:200]}"
    body = r.json()
    writeback = body.get("writeback")
    assert writeback in ("proposal_created", "pending"), (
        f"writeback must be proposal_created/pending under review_required; "
        f"got {writeback!r}"
    )


@pytest.mark.level3
@pytest.mark.requires_provider
def test_propose_update_forbidden_when_writeback_forbidden(provider_url):
    """If provider has a separate PPX_FORBIDDEN_WRITEBACK_TOKEN (grant with
    writeback_policy=forbidden), propose_updates MUST be rejected."""
    import os
    import httpx
    token = os.environ.get("PPX_FORBIDDEN_WRITEBACK_TOKEN")
    if not token:
        pytest.skip("PPX_FORBIDDEN_WRITEBACK_TOKEN not set — skipping")
    r = httpx.post(
        f"{provider_url}/v1/profile/propose-updates",
        json={"claims": []},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10.0,
    )
    assert r.status_code in (403, 409), (
        f"forbidden writeback MUST return 403/409; got {r.status_code}"
    )
