"""L1: the HTTP binding's profile-read routes actually exist and behave.

Every one of these endpoints is normative in `bindings/http.md`, and none of
them had conformance coverage. The reference provider shipped without
`/v1/profile/summary` and `/v1/profile/query` at all, and the SDKs shipped a
`my_profile()` pointed at `/v1/profile/me` — a path in neither the spec nor any
implementation. All of it went unnoticed because the suite only ever exercised
`/v1/profile/effective`.

A binding entry no test touches is a suggestion, not a requirement.
"""
import pytest


@pytest.mark.level1
@pytest.mark.requires_provider
def test_profile_summary_exists_and_redacts_values(provider_client):
    """GET /v1/profile/summary MUST exist and MUST NOT disclose claim values.

    The binding calls this a *redacted* summary. Redaction is the entire
    reason the endpoint is cheaper than the effective read — a provider that
    returns values here has built an unaudited alias of `/v1/profile/effective`
    while advertising something safer.
    """
    r = provider_client.get("/v1/profile/summary")
    assert r.status_code == 200, (
        f"/v1/profile/summary is normative in the HTTP binding; "
        f"got {r.status_code}: {r.text[:200]}"
    )
    body = r.json()

    claims = body.get("claims")
    assert isinstance(claims, list), "summary MUST carry a `claims` array"

    leaked = [c for c in claims if isinstance(c, dict) and "value" in c]
    assert not leaked, (
        f"{len(leaked)} of {len(claims)} summary claims disclose a `value`; "
        "the summary MUST be redacted"
    )

    # Redacted does not mean useless: a caller has to be able to tell which
    # claims exist in order to decide what to request.
    for c in claims:
        assert "key" in c, f"summary claim without a `key`: {c}"


@pytest.mark.level1
@pytest.mark.requires_provider
def test_profile_query_returns_an_effective_profile_document(provider_client):
    """POST /v1/profile/query MUST return an effective-profile document.

    The binding is explicit that query and effective share a response schema.
    Required: ppx_version, subject_id, provider_id, generated_at, claims,
    applied_modifiers.
    """
    r = provider_client.post("/v1/profile/query", json={})
    assert r.status_code == 200, (
        f"/v1/profile/query is normative in the HTTP binding; "
        f"got {r.status_code}: {r.text[:200]}"
    )
    body = r.json()

    for field in (
        "ppx_version",
        "subject_id",
        "provider_id",
        "generated_at",
        "claims",
        "applied_modifiers",
    ):
        assert field in body, f"query response is missing required field `{field}`"

    assert isinstance(body["claims"], list)
    assert isinstance(body["applied_modifiers"], list), (
        "`applied_modifiers` is REQUIRED and MAY be empty — an absent array is "
        "not the same as an empty one"
    )


@pytest.mark.level1
@pytest.mark.requires_provider
def test_query_never_widens_the_grant(provider_client):
    """A narrowing request MUST NOT return more than the unnarrowed one.

    Filtering is an intersection with the grant. A provider that treats
    `requested_namespaces` as a selector rather than a narrowing could return
    claims outside the grant when asked for a namespace it does not cover.
    """
    everything = provider_client.post("/v1/profile/query", json={})
    assert everything.status_code == 200
    baseline = {
        (c.get("namespace"), c.get("key")) for c in everything.json().get("claims", [])
    }

    narrowed = provider_client.post(
        "/v1/profile/query", json={"requested_namespaces": ["core"]}
    )
    assert narrowed.status_code == 200
    got = {(c.get("namespace"), c.get("key")) for c in narrowed.json().get("claims", [])}

    assert got <= baseline, (
        f"narrowing to `core` returned claims absent from the unnarrowed read: "
        f"{sorted(got - baseline)}"
    )
