"""Tests for lodkit.NamespaceGraph."""

from types import new_class

from hypothesis import given
from lodkit import NamespaceGraph
import pytest
from rdflib import URIRef
from tests.utils.strategies import (
    fail_pairs,
    name_namespace_pairs,
    name_uri_pairs,
    name_uriref_pairs,
)
from typeguard import TypeCheckError


def _namespacegraph_containment_helper(assignment_pair: tuple[str, str]):
    """Helper for NamespaceGraph containment checks."""
    name, namespace = assignment_pair
    NamespaceGraphCls = new_class(
        "NamespaceGraphCls",
        bases=(NamespaceGraph,),
        exec_body=lambda ns: ns.update({name: namespace}),
    )

    nscls = NamespaceGraphCls()

    assert assignment_pair in NamespaceGraphCls.__dict__.items()
    assert (name, URIRef(namespace)) in list(nscls.namespaces())


@given(name_namespace_pairs)
def test_namespacegraph_str_ns_containment(pair):
    """Check if asserted str/rdflib.Namespace pairs are in cls.__dict__ and Graph.namespaces."""
    _namespacegraph_containment_helper(pair)


@given(name_uri_pairs)
def test_namespacegraph_str_uri_containment(pair):
    """Check if asserted str/URI pairs are in cls.__dict__ and Graph.namespaces."""
    _namespacegraph_containment_helper(pair)


@given(name_uriref_pairs)
def test_namespacegraph_str_uriref_containment(pair):
    """Check if asserted str/URIRef pairs are in cls.__dict__ and Graph.namespaces."""
    _namespacegraph_containment_helper(pair)


@given(fail_pairs)
def test_fail_on_value(pair):
    """Check if type-invalid inputs cause a TypeCheckError."""
    with pytest.raises(TypeCheckError):
        name, namespace = pair
        new_class(
            "NamespaceGraphCls",
            bases=(NamespaceGraph,),
            exec_body=lambda ns: ns.update({name: namespace}),
        )
