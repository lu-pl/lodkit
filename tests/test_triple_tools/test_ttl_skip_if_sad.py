"""Happy path tests for the skip_if feature of lodkit.ttl."""

import pytest

from lodkit import ttl
from rdflib import URIRef


fail_objects = [None, type("CustomType", (), {})]


@pytest.mark.parametrize("obj", fail_objects)
def test_ttl_type_error(obj):
    """Check if default clause of the ttl.__iter__ switch raises a TypeEror.

    This covers the case where runtime checking is deactivated by passing a skip_if callable.
    Note though that only the triple object is checked in that case then
    and this form of checking is generally weaker than the typeguard runtime checks.
    """
    triples = ttl(
        URIRef("subject"), (URIRef("prdicate"), obj), skip_if=lambda s, p, o: False
    )

    with pytest.raises(TypeError):
        list(triples)
