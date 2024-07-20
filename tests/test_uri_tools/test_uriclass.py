"""Test for lodkit.uri_tools.uriclass."""

from types import new_class

from hypothesis import given, strategies as st
from lodkit import make_uriclass, mkuri_factory, uriclass
import pytest
from rdflib import Namespace, URIRef
from tests.utils.strategies.ns_strategies import public_variable_names


@given(public_variable_names, st.text())
def test_uriclass_hashed(variable_name, hash_value):
    """Check if hashed URIs generated with uriclass and mkuri_factory are equal."""
    namespace = Namespace("https://lodkit.testing/")
    mkuri = mkuri_factory(namespace)

    _uriclass_constructor = uriclass(namespace)
    uricls = _uriclass_constructor(
        new_class(
            "_uriclass", exec_body=lambda ns: ns.update({variable_name: hash_value})
        )
    )

    hashed_uri = getattr(uricls, variable_name)
    assert hashed_uri == mkuri(hash_value)


@given(public_variable_names)
def test_uriclass_uuids(variable_name):
    """Test uriclass UUID URI generation."""
    namespace = Namespace("https://lodkit.testing/")
    annotations = {variable_name: URIRef}

    _uriclass_constructor = uriclass(namespace)
    uricls = _uriclass_constructor(
        new_class(
            "_uriclass",
            exec_body=lambda ns: ns.update({"__annotations__": annotations}),
        )
    )

    assert uricls


@given(public_variable_names, st.text())
def test_make_uriclass_hashed(variable_name, hash_value):
    """Check if hashed URIs generated with make_uriclass and mkuri_factory are equal."""
    namespace = Namespace("https://lodkit.testing/")
    mkuri = mkuri_factory(namespace)

    uricls = make_uriclass("uricls", namespace, fields=((variable_name, hash_value),))

    hashed_uri = getattr(uricls, variable_name)
    assert hashed_uri == mkuri(hash_value)


@given(public_variable_names)
def test_make_uriclass_uuids(variable_name):
    """Test make_uriclass UUID URI generation."""
    namespace = Namespace("https://lodkit.testing/")
    uricls = make_uriclass("uricls", namespace, fields=(variable_name))
    assert uricls


@pytest.mark.parametrize("x, y", ((1, "test"), ("test", 1), (1, 2)))
def test_make_uriclass_generate_pairs_type_fail(x, y):
    """Simple case for triggering a TyperError in make_uriclass."""
    with pytest.raises(TypeError):
        namespace = Namespace("https://lodkit.testing/")
        uricls = make_uriclass("uricls", namespace, fields=((x, y),))
