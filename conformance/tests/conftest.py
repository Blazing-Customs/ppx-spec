import json
import os
from pathlib import Path

import httpx
import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

SPEC_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_ROOT = SPEC_ROOT / "schemas"
EXAMPLES_ROOT = SPEC_ROOT / "examples"


@pytest.fixture(scope="session")
def schema_registry() -> Registry:
    resources = []
    for schema_file in (SCHEMAS_ROOT / "core").glob("*.schema.json"):
        with open(schema_file) as f:
            schema = json.load(f)
        resources.append((schema["$id"], Resource(contents=schema, specification=DRAFT202012)))
    return Registry().with_resources(resources)


@pytest.fixture(scope="session")
def core_schemas() -> dict:
    out = {}
    for schema_file in (SCHEMAS_ROOT / "core").glob("*.schema.json"):
        with open(schema_file) as f:
            schema = json.load(f)
        out[schema_file.stem] = schema
    return out


def _validator(schema, registry):
    return Draft202012Validator(schema, registry=registry)


@pytest.fixture(scope="session")
def validate(schema_registry):
    def _do(schema: dict, instance) -> list[str]:
        errs = list(_validator(schema, schema_registry).iter_errors(instance))
        return [f"{list(e.absolute_path)}: {e.message}" for e in errs]
    return _do


# ---------- provider fixtures ----------

def _require_provider() -> str | None:
    return os.environ.get("PPX_PROVIDER_URL")


@pytest.fixture(scope="session")
def provider_url() -> str:
    url = _require_provider()
    if not url:
        pytest.skip("PPX_PROVIDER_URL not set — skipping provider-backed tests.")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def provider_token() -> str:
    token = os.environ.get("PPX_PROVIDER_TOKEN")
    if not token:
        pytest.skip("PPX_PROVIDER_TOKEN not set — skipping authenticated tests.")
    return token


@pytest.fixture
def provider_client(provider_url, provider_token):
    with httpx.Client(
        base_url=provider_url,
        headers={"Authorization": f"Bearer {provider_token}"},
        timeout=10.0,
    ) as client:
        yield client


# ---------- spec-local fixtures ----------

@pytest.fixture(scope="session")
def example_profile():
    with open(EXAMPLES_ROOT / "profile-basic.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def example_grant_fragrance():
    with open(EXAMPLES_ROOT / "grant-fragrance.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def example_grant_travel():
    with open(EXAMPLES_ROOT / "grant-travel.json") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def example_discovery_card():
    with open(EXAMPLES_ROOT / "discovery-card.json") as f:
        return json.load(f)
