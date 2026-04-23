"""L1: Provider serves a valid discovery card at /.well-known/ppx-card.json."""
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_discovery_card_present_and_valid(provider_url, validate, core_schemas):
    import httpx

    r = httpx.get(f"{provider_url}/.well-known/ppx-card.json", timeout=10.0)
    assert r.status_code == 200, f"discovery card returned {r.status_code}"
    assert r.headers.get("content-type", "").startswith("application/json")
    card = r.json()
    errors = validate(core_schemas["discovery-card.schema"], card)
    assert not errors, "discovery card failed schema validation:\n" + "\n".join(errors)


@pytest.mark.level1
@pytest.mark.requires_provider
def test_discovery_card_declares_supported_namespaces(provider_url):
    import httpx

    r = httpx.get(f"{provider_url}/.well-known/ppx-card.json", timeout=10.0)
    card = r.json()
    assert "core" in card["supported_namespaces"], (
        "every conforming provider MUST support the core namespace"
    )


@pytest.mark.level1
@pytest.mark.requires_provider
def test_discovery_card_advertises_auth(provider_url):
    import httpx

    r = httpx.get(f"{provider_url}/.well-known/ppx-card.json", timeout=10.0)
    card = r.json()
    assert card["auth"]["schemes"], "auth.schemes MUST be non-empty"
