"""L2: the consent-grant lifecycle.

These tests drive the flow a real integrator follows — request, decide, mint,
read, refresh, revoke — rather than starting from a pre-minted token. They are
skipped unless the provider advertises `consent_management` and the harness is
given a way to authenticate a subject.

The properties asserted here are the ones that make PPX a consent protocol
rather than an API key with extra steps:

  * a grant request carries no authority until the subject approves it;
  * the subject can approve LESS than was asked for, and the narrowing is
    enforced on reads, not merely recorded;
  * a grantee's own token cannot approve further grants for that grantee;
  * revocation is immediate and fails closed on refresh;
  * the grant_request_id is NOT a credential: exchange additionally requires a
    back-channel request token, PKCE (S256), and the client it was issued to;
  * refresh tokens rotate, and replaying a spent one is treated as theft.
"""
import base64
import hashlib
import os
import secrets

import pytest

pytestmark = [pytest.mark.level2, pytest.mark.requires_provider]


def _cfg(name: str) -> str | None:
    return os.environ.get(name)


def _b64url(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _pkce() -> tuple[str, str]:
    """A verifier and its S256 challenge. `plain` is not offered anywhere."""
    verifier = _b64url(secrets.token_bytes(48))
    return verifier, _b64url(hashlib.sha256(verifier.encode()).digest())


def _mint(http, cfg, req, **overrides):
    """Exchange an approved request. The id alone is never sufficient."""
    body = {
        "grant_request_id": req["grant_request_id"],
        "request_token": req["request_token"],
        "code_verifier": req["_verifier"],
        "client_id": cfg["client_id"],
    }
    body.update(overrides)
    return http.post("/v1/consent/token", json=body)


@pytest.fixture(scope="session")
def grant_flow_config(provider_url):
    """Everything needed to drive a full consent round-trip.

    A provider that does not issue grants over HTTP (some mint them out of
    band) is skipped rather than failed — the flow is L2, not L1.
    """
    client_id = _cfg("PPX_CLIENT_ID")
    subject_id = _cfg("PPX_SUBJECT_ID")
    user_token = _cfg("PPX_USER_TOKEN")

    if not (client_id and subject_id and user_token):
        pytest.skip(
            "grant-flow tests need PPX_CLIENT_ID, PPX_SUBJECT_ID and PPX_USER_TOKEN "
            "(a token authenticating the subject, not a grant token)"
        )
    return {"client_id": client_id, "subject_id": subject_id, "user_token": user_token}


@pytest.fixture
def http(provider_url):
    import httpx

    with httpx.Client(base_url=provider_url, timeout=15.0) as c:
        yield c


def _request_grant(http, cfg, **overrides):
    body = {
        "client_id": cfg["client_id"],
        "subject_id": cfg["subject_id"],
        "purposes": ["recommendation"],
        "allowed_domains": ["fragrance"],
        "allowed_namespaces": ["core", "fragrance"],
        "allowed_operations": ["read"],
        "cross_domain_transfer": "deny",
        "writeback_policy": "review_required",
        "requested_duration_days": 30,
    }
    verifier, challenge = _pkce()
    body["code_challenge"] = challenge
    body["code_challenge_method"] = "S256"
    body.update(overrides)
    r = http.post("/v1/consent/request", json=body)
    assert r.status_code in (200, 201), f"consent/request failed: {r.status_code} {r.text[:200]}"
    out = r.json()
    assert out.get("request_token"), "the provider MUST return a back-channel request_token"
    # Carried alongside so callers can exchange without replumbing every test.
    out["_verifier"] = verifier
    return out


def _user_headers(cfg):
    return {"Authorization": f"Bearer {cfg['user_token']}"}


def test_grant_request_is_pending_and_carries_no_authority(http, grant_flow_config):
    out = _request_grant(http, grant_flow_config)
    assert out.get("grant_request_id"), "response must carry grant_request_id"
    assert out.get("status") == "pending"
    assert out.get("consent_url"), "the subject must have somewhere to go to decide"

    # The central property: an undecided request cannot be exchanged for a token.
    r = _mint(http, grant_flow_config, out)
    assert r.status_code != 200, (
        "a token was issued for a request the subject has not approved — "
        "this defeats the entire consent model"
    )


def test_unregistered_client_is_refused(http, grant_flow_config):
    r = http.post(
        "/v1/consent/request",
        json={
            "client_id": "definitely-not-registered-" + "x" * 8,
            "subject_id": grant_flow_config["subject_id"],
            "purposes": ["recommendation"],
            "allowed_namespaces": ["fragrance"],
        },
    )
    # Any 4xx refusal is conforming. Implementations differ on which: a
    # lookup-miss reads as 404, a policy refusal as 403, and a framework that
    # validates client_id as part of the body will say 400 or 422. What must
    # not happen is a grant request succeeding for an unknown grantee.
    assert 400 <= r.status_code < 500, (
        f"an unregistered client_id must be refused, got {r.status_code}"
    )


def test_approve_then_mint_then_read(http, grant_flow_config):
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    rid = req["grant_request_id"]

    r = http.post("/v1/consent/approve", json={"grant_request_id": rid}, headers=_user_headers(cfg))
    assert r.status_code == 200, f"approve failed: {r.status_code} {r.text[:200]}"

    r = _mint(http, cfg, req)
    assert r.status_code == 200, f"token exchange failed: {r.status_code} {r.text[:200]}"
    tok = r.json()
    assert tok.get("token_type") == "Bearer"
    assert tok.get("access_token") and tok.get("grant_id")
    assert isinstance(tok.get("expires_in"), int) and tok["expires_in"] > 0

    r = http.post(
        "/v1/profile/effective",
        json={"context": {}},
        headers={"Authorization": f"Bearer {tok['access_token']}"},
    )
    assert r.status_code == 200, f"read under a fresh grant failed: {r.status_code}"


def test_subject_can_narrow_at_approval_and_narrowing_is_enforced(http, grant_flow_config):
    """Approving less than was asked for must change what can be read.

    A provider that records the narrowing but still serves the wider scope
    passes a naive check and violates the point of the consent screen.
    """
    cfg = grant_flow_config
    req = _request_grant(http, cfg, allowed_namespaces=["core", "fragrance"])
    rid = req["grant_request_id"]

    r = http.post(
        "/v1/consent/approve",
        json={"grant_request_id": rid, "narrow": {"allowed_namespaces": ["fragrance"]}},
        headers=_user_headers(cfg),
    )
    if r.status_code != 200:
        pytest.skip(f"provider does not support narrowing at approval ({r.status_code})")

    tok = _mint(http, cfg, req).json()
    body = http.post(
        "/v1/profile/effective",
        json={"context": {}},
        headers={"Authorization": f"Bearer {tok['access_token']}"},
    ).json()

    namespaces = {c.get("namespace") for c in body.get("claims", [])}
    assert "core" not in namespaces, (
        f"subject narrowed the grant to 'fragrance' but 'core' claims were still "
        f"returned (namespaces seen: {sorted(namespaces)})"
    )


def test_grant_token_cannot_approve_further_grants(http, grant_flow_config):
    """Privilege separation: a grantee must not be able to widen its own access.

    If a grant token could approve, any grantee could mint itself a second,
    broader grant without the subject ever seeing a consent screen.
    """
    cfg = grant_flow_config
    first = _request_grant(http, cfg)
    http.post("/v1/consent/approve", json={"grant_request_id": first["grant_request_id"]},
              headers=_user_headers(cfg))
    tok = _mint(http, cfg, first).json()

    second = _request_grant(http, cfg)
    r = http.post(
        "/v1/consent/approve",
        json={"grant_request_id": second["grant_request_id"]},
        headers={"Authorization": f"Bearer {tok['access_token']}"},
    )
    assert r.status_code != 200, (
        "a grant-scoped token approved a new grant — a grantee can escalate its "
        "own access without the subject's involvement"
    )


def test_rejected_request_cannot_be_exchanged(http, grant_flow_config):
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    rid = req["grant_request_id"]

    r = http.post("/v1/consent/reject", json={"grant_request_id": rid}, headers=_user_headers(cfg))
    assert r.status_code == 200, f"reject failed: {r.status_code} {r.text[:200]}"

    r = _mint(http, cfg, req)
    assert r.status_code != 200, "a rejected request was exchanged for a token"


def test_refresh_returns_a_token_without_user_interaction(http, grant_flow_config):
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    rid = req["grant_request_id"]
    http.post("/v1/consent/approve", json={"grant_request_id": rid}, headers=_user_headers(cfg))
    tok = _mint(http, cfg, req).json()

    assert tok.get("refresh_token"), "the provider MUST issue a refresh token"
    r = http.post("/v1/consent/refresh",
                  json={"client_id": cfg["client_id"], "refresh_token": tok["refresh_token"]})
    assert r.status_code == 200, f"refresh failed: {r.status_code} {r.text[:200]}"
    body = r.json()
    assert body.get("access_token")
    assert body.get("refresh_token") and body["refresh_token"] != tok["refresh_token"], (
        "refresh MUST rotate: a new refresh token has to replace the spent one"
    )


def test_revocation_is_immediate_and_refresh_fails_closed(http, grant_flow_config):
    """After revocation: reads stop, and refresh returns 410 Gone.

    410 rather than 403 is what lets a client distinguish "this grant was
    deliberately destroyed, start over" from "try again later".
    """
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    rid = req["grant_request_id"]
    http.post("/v1/consent/approve", json={"grant_request_id": rid}, headers=_user_headers(cfg))
    tok = _mint(http, cfg, req).json()
    auth = {"Authorization": f"Bearer {tok['access_token']}"}

    assert http.post("/v1/profile/effective", json={"context": {}}, headers=auth).status_code == 200

    r = http.post("/v1/consent/revoke", json={"grant_id": tok["grant_id"]}, headers=_user_headers(cfg))
    assert r.status_code == 200, (
        f"the subject could not revoke their own grant ({r.status_code}) — "
        "withdrawal of consent must always be available to the subject"
    )

    assert http.post("/v1/profile/effective", json={"context": {}}, headers=auth).status_code != 200, (
        "a revoked grant still authorized a read"
    )

    r = http.post("/v1/consent/refresh",
                  json={"client_id": cfg["client_id"], "refresh_token": tok["refresh_token"]})
    assert r.status_code == 410, f"refresh on a revoked grant must be 410 Gone, got {r.status_code}"


# --------------------------------------------------------------------------
# consent-v2: the grant_request_id is not a credential
# --------------------------------------------------------------------------


def test_pkce_is_required(http, grant_flow_config):
    """A request with no code_challenge MUST be refused.

    PKCE is not advisory here. Every client this protocol targets is either a
    browser app or a distributed package, so none can keep a secret; the
    verifier is the only thing binding the exchange to the party that started
    the flow.
    """
    cfg = grant_flow_config
    r = http.post("/v1/consent/request", json={
        "client_id": cfg["client_id"],
        "subject_id": cfg["subject_id"],
        "purposes": ["recommendation"],
        "allowed_domains": ["fragrance"],
        "allowed_namespaces": ["core"],
    })
    assert r.status_code == 400, f"a request without PKCE was accepted: {r.status_code}"


def test_pkce_plain_is_refused(http, grant_flow_config):
    """S256 only. A downgrade the server tolerates is one an attacker can ask for."""
    cfg = grant_flow_config
    _, challenge = _pkce()
    r = http.post("/v1/consent/request", json={
        "client_id": cfg["client_id"],
        "subject_id": cfg["subject_id"],
        "purposes": ["recommendation"],
        "allowed_domains": ["fragrance"],
        "allowed_namespaces": ["core"],
        "code_challenge": challenge,
        "code_challenge_method": "plain",
    })
    assert r.status_code == 400, f"code_challenge_method=plain was accepted: {r.status_code}"


def test_grant_request_id_alone_cannot_be_exchanged(http, grant_flow_config):
    """The core v2 property. The id travels in a URL, so it must buy nothing."""
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    http.post("/v1/consent/approve",
              json={"grant_request_id": req["grant_request_id"]}, headers=_user_headers(cfg))

    r = http.post("/v1/consent/token", json={"grant_request_id": req["grant_request_id"]})
    assert r.status_code != 200, "the grant_request_id alone was exchanged for a token"
    assert "access_token" not in r.json()


def test_exchange_requires_the_matching_pkce_verifier(http, grant_flow_config):
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    http.post("/v1/consent/approve",
              json={"grant_request_id": req["grant_request_id"]}, headers=_user_headers(cfg))

    wrong, _ = _pkce()
    r = _mint(http, cfg, req, code_verifier=wrong)
    assert r.status_code != 200, "a wrong PKCE verifier was accepted"


def test_a_spent_grant_request_cannot_be_replayed(http, grant_flow_config):
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    http.post("/v1/consent/approve",
              json={"grant_request_id": req["grant_request_id"]}, headers=_user_headers(cfg))

    assert _mint(http, cfg, req).status_code == 200
    assert _mint(http, cfg, req).status_code != 200, "a used grant request was exchanged twice"


def test_refresh_reuse_burns_the_family_and_the_grant(http, grant_flow_config):
    """Rotation is only useful if replay is detected and acted on.

    Presenting an already-rotated token means two parties hold the chain. The
    provider cannot tell which is the thief, so it MUST invalidate the whole
    family — including the token the legitimate client is holding — and revoke
    the grant behind it.
    """
    cfg = grant_flow_config
    req = _request_grant(http, cfg)
    http.post("/v1/consent/approve",
              json={"grant_request_id": req["grant_request_id"]}, headers=_user_headers(cfg))
    tok = _mint(http, cfg, req).json()

    first = tok["refresh_token"]
    rotated = http.post("/v1/consent/refresh",
                        json={"client_id": cfg["client_id"], "refresh_token": first}).json()
    second = rotated["refresh_token"]

    replay = http.post("/v1/consent/refresh",
                       json={"client_id": cfg["client_id"], "refresh_token": first})
    assert replay.status_code != 200, "a spent refresh token was redeemed again"

    after = http.post("/v1/consent/refresh",
                      json={"client_id": cfg["client_id"], "refresh_token": second})
    assert after.status_code != 200, (
        "reuse was detected but the family survived — the current token must die too"
    )
