"""L1: Response payloads never include claim keys outside a grant's scope."""
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_response_claims_within_grant_scope(provider_client):
    """get_effective_profile returns only claims within `allowed_claim_keys`.

    This test assumes the provider_token is bound to a grant with a known
    `allowed_claim_keys` list; the provider is expected to echo that list in
    a `grant` block of the response (or in an `X-PPX-Grant-Id` header) so the
    test can introspect it.
    """
    r = provider_client.post("/v1/profile/effective", json={"context": {}})
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text[:200]}"
    body = r.json()

    # Provider SHOULD echo the grant scope under `grant` for auditability.
    grant = body.get("grant") or {}
    allowed_keys = set(grant.get("allowed_claim_keys") or [])
    allowed_ns = set(grant.get("allowed_namespaces") or [])

    if not allowed_keys and not allowed_ns:
        pytest.skip(
            "provider did not echo grant scope; cannot verify redaction — "
            "provider SHOULD include a `grant` block for auditability"
        )

    for claim in body.get("claims", []):
        ns = claim.get("namespace")
        key = claim.get("key")
        fq = f"{ns}.{key}" if ns != "core" else key
        in_keys = (key in allowed_keys) or (fq in allowed_keys)
        in_ns = ns in allowed_ns
        assert in_keys or in_ns, (
            f"claim {ns}.{key} returned outside of grant scope "
            f"(allowed_claim_keys={allowed_keys}, allowed_namespaces={allowed_ns})"
        )
