"""Tests for lodkit.uri_tools.uribase."""

from types import new_class

from hypothesis import given, strategies as st
from lodkit import mkuri_factory, uribase
from rdflib import Namespace, URIRef
from tests.utils.strategies.ns_strategies import public_variable_names


@given(public_variable_names)
def test_uribase_uuids(variable_name):
    """Check if a uribase base class constructs UUID URIs for 'loose' class attributes.

    Note: This is awkward to test and awkward to use and probably not a good idea anyways.
    """
    uribase_code: str = f"""class uribase_cls(uribase(Namespace('https://lodkit.testing/'))):
    {variable_name}"""

    exec(uribase_code, globals())
    uri = getattr(uribase_cls, variable_name)

    assert isinstance(uri, URIRef)


@given(public_variable_names, st.text())
def test_uribase_hashed(variable_name, hash_value):
    """Check if uribase and mkuri_factory constructed hashed URIs are equal."""
    namespace = Namespace("https://lodkit.testing/")
    mkuri = mkuri_factory(namespace)

    uribase_cls = new_class(
        "uribase_cls",
        bases=(uribase(namespace),),
        exec_body=lambda ns: ns.update({variable_name: hash_value}),
    )

    assert getattr(uribase_cls, variable_name) == mkuri(hash_value)
