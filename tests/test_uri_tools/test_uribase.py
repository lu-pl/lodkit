"""Tests for lodkit.uri_tools.uribase."""

from types import new_class

from hypothesis import given, strategies as st
from lodkit import mkuri_factory, uribase
from lodkit.uri_tools.uribase import InstantiationException
import pytest
from rdflib import Namespace
from tests.utils.strategies.ns_strategies import public_variable_names


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


@given(public_variable_names, st.text())
def test_uribase_instantiation_fail(variable_name, hash_value):
    """Check if uribase and mkuri_factory constructed hashed URIs are equal."""
    namespace = Namespace("https://lodkit.testing/")
    mkuri_factory(namespace)

    uribase_cls = new_class(
        "uribase_cls",
        bases=(uribase(namespace),),
        exec_body=lambda ns: ns.update({variable_name: hash_value}),
    )

    with pytest.raises(InstantiationException):
        uribase_cls()
