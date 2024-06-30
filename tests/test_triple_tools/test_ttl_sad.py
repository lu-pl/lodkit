"""Sad path tests for ttl triple constructor."""

import pytest
from typeguard import TypeCheckError

from hypothesis import given
from lodkit import ttl
from rdflib import BNode
from tests.utils.strategies import (
    fail_object_pairs,
    fail_predicate_pairs,
    fail_uris,
    predicate_object_pairs,
)


@given(uri=fail_uris, pair=predicate_object_pairs)
def test_ttl_fail_type_uri_parameter(uri, pair):
    """Check if ttl raises TypeCheckError with invalid uri parameter types."""
    with pytest.raises(TypeCheckError):
        ttl(uri, pair)


@given(pair=fail_predicate_pairs)
def test_ttl_fail_type_predicate(pair):
    """Check if ttl raises TypeCheckError with invalid predicate in predicate_object_pairs parameter."""
    with pytest.raises(TypeCheckError):
        ttl(BNode(), pair)


@given(pair=fail_object_pairs)
def test_ttl_fail_type_object(pair):
    """Check if ttl raises TypeCheckError with invalid object in predicate_object_pairs parameter."""
    with pytest.raises(TypeCheckError):
        ttl(BNode(), pair)
