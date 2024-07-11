"""Sad path tests for ttl triple constructor."""

from hypothesis import given
from lodkit import ttl
import pytest
from rdflib import BNode
from tests.utils.fixtures import constructor
from tests.utils.strategies import (
    fail_object_pairs,
    fail_predicate_pairs,
    fail_uris,
    predicate_object_pairs,
)
from typeguard import TypeCheckError


@given(uri=fail_uris, pair=predicate_object_pairs)
def test_ttl_fail_type_uri_parameter(uri, pair, constructor):
    """Check if ttl raises TypeCheckError with invalid uri parameter types."""
    with pytest.raises(TypeCheckError):
        constructor(uri, pair)


@given(pair=fail_predicate_pairs)
def test_ttl_fail_type_predicate(pair, constructor):
    """Check if ttl raises TypeCheckError with invalid predicate in predicate_object_pairs parameter."""
    with pytest.raises(TypeCheckError):
        constructor(BNode(), pair)


@given(pair=fail_object_pairs)
def test_ttl_fail_type_object(pair, constructor):
    """Check if ttl raises TypeCheckError with invalid object in predicate_object_pairs parameter."""
    with pytest.raises(TypeCheckError):
        constructor(BNode(), pair)
