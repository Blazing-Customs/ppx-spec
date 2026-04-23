"""SCHEMA: every example payload validates against its declared schema."""
from pathlib import Path

import pytest

from .conftest import EXAMPLES_ROOT

EXAMPLE_TO_SCHEMA = {
    "profile-basic.json": "profile",
    "grant-fragrance.json": "consent-grant",
    "grant-travel.json": "consent-grant",
    "derived-view-dating.json": "derived-view",
    "discovery-card.json": "discovery-card",
    "context-modifier-climate.json": "context-modifier",
}


@pytest.mark.schema
@pytest.mark.parametrize("example_file,schema_stem", sorted(EXAMPLE_TO_SCHEMA.items()))
def test_example_validates_against_schema(validate, core_schemas, example_file, schema_stem):
    """Every bundled example MUST validate against its corresponding schema."""
    import json

    with open(EXAMPLES_ROOT / example_file) as f:
        instance = json.load(f)
    schema = core_schemas[f"{schema_stem}.schema"]
    errors = validate(schema, instance)
    assert not errors, f"{example_file} failed validation:\n" + "\n".join(errors)


@pytest.mark.schema
def test_all_core_schemas_are_valid_schemas(core_schemas):
    """Every core schema must itself be a valid JSON Schema 2020-12 document."""
    from jsonschema import Draft202012Validator
    for name, schema in core_schemas.items():
        Draft202012Validator.check_schema(schema)
