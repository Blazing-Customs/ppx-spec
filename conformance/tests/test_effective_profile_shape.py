"""L1: the effective-profile response conforms to its schema.

This test exists because its absence let two independent implementations
disagree on the response body while both passed the suite. The Python
reference provider returned `profile_id` and no `subject_id`; the PHP
provider returned `subject_id`/`provider_id`/`generated_at` and no
`profile_id`. A client written against either broke against the other.

The shape is now pinned by effective-profile.schema.json and bindings/http.md.
"""
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_effective_profile_matches_schema(provider_client, core_schemas, validate):
    r = provider_client.post("/v1/profile/effective", json={"context": {}})
    assert r.status_code == 200, f"expected 200, got {r.status_code}: {r.text[:200]}"

    errors = validate(core_schemas["effective-profile.schema"], r.json())
    assert not errors, "effective-profile response violates its schema:\n  " + "\n  ".join(errors)


@pytest.mark.level1
@pytest.mark.requires_provider
def test_effective_profile_reports_applied_modifiers_explicitly(provider_client):
    """`applied_modifiers` MUST be present, even when empty.

    Omitting it is indistinguishable from "this provider does not report
    modifiers", which defeats the explainability the field exists for.
    """
    body = provider_client.post("/v1/profile/effective", json={"context": {}}).json()
    assert "applied_modifiers" in body, (
        "`applied_modifiers` is required and MAY be empty; omitting it hides "
        "whether modifiers were considered at all"
    )
    assert isinstance(body["applied_modifiers"], list)


@pytest.mark.level1
@pytest.mark.requires_provider
def test_effective_profile_identifies_subject_and_provider(provider_client):
    """A grantee holding several grants must be able to tell responses apart
    without relying on request/response ordering."""
    body = provider_client.post("/v1/profile/effective", json={"context": {}}).json()
    assert body.get("subject_id"), "`subject_id` is required"
    assert body.get("provider_id"), "`provider_id` is required"
    assert body.get("generated_at"), "`generated_at` is required — resolved views are time-dependent"


@pytest.mark.level1
@pytest.mark.requires_provider
def test_requested_namespaces_narrows_the_response(provider_client):
    """A caller may ask for LESS than the grant permits, and MUST get less.

    Returning everything in grant scope regardless of what was requested is
    over-disclosure: technically authorized, but it defeats data minimisation
    and means a client cannot limit its own exposure.
    """
    everything = provider_client.post("/v1/profile/effective", json={"context": {}}).json()
    all_ns = {c.get("namespace") for c in everything.get("claims", [])}
    if len(all_ns) < 2:
        pytest.skip(f"grant only covers {all_ns}; need two namespaces to test narrowing")

    target = sorted(all_ns)[0]
    narrowed = provider_client.post(
        "/v1/profile/effective",
        json={"context": {}, "requested_namespaces": [target]},
    ).json()

    got = {c.get("namespace") for c in narrowed.get("claims", [])}
    assert got <= {target}, (
        f"requested only {target!r} but the response also contained "
        f"{sorted(got - {target})} — the request must narrow, never be ignored"
    )
