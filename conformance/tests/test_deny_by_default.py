"""L1: Access without an active grant is denied (deny-by-default)."""
import httpx
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_unauthenticated_request_denied(provider_url):
    """Requests without any bearer token MUST NOT return profile data."""
    r = httpx.post(
        f"{provider_url}/v1/profile/effective",
        json={"context": {}},
        timeout=10.0,
    )
    assert r.status_code in (401, 403), (
        f"expected 401/403 for unauthenticated request, got {r.status_code}"
    )


@pytest.mark.level1
@pytest.mark.requires_provider
def test_invalid_token_denied(provider_url):
    r = httpx.post(
        f"{provider_url}/v1/profile/effective",
        json={"context": {}},
        headers={"Authorization": "Bearer invalid-token-xxxx"},
        timeout=10.0,
    )
    assert r.status_code in (401, 403)
