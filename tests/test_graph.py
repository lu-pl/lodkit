"""Pytest entry point for lodkit.Graph tests."""

from lodkit.graph import Graph

from rdflib import Namespace
from rdflib.namespace import OWL, RDFS, RDF

ex = Namespace("http://example.org/")


def get_test_graph() -> Graph:
    """Generate a fresh test graph."""

    graph = Graph()
    graph.add((ex.s, ex.p, ex.o))

    # subclass: ex.individual should be inferred to be also of type ex.supersubj
    graph.add((ex.s, RDFS.subClassOf, ex.super))
    graph.add((ex.individual, RDF.type, ex.s))

    # inverse: (ex.o, ex.pInverse, x.s) should be inferred
    graph.add((ex.pInverse, OWL.inverseOf, ex.p))

    return graph


def test_rdfs_subclass():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.individual, RDF.type, ex.super))

    inferred_graph = test_graph.inference("rdfs")

    assert expected_inference in inferred_graph


def test_rdfs_inverse():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.o, ex.pInverse, ex.s))

    inferred_graph = test_graph.inference("rdfs")

    # should NOT be in the graph since inverseOf requires OWL reasoning
    assert expected_inference not in inferred_graph


def test_owlrl_subclass():
    """Run reasoner and check if expected inference is in the inferred graph."""
    test_graph = get_test_graph()
    expected_inference = ((ex.individual, RDF.type, ex.super))

    inferred_graph = test_graph.inference("owlrl")

    assert expected_inference in inferred_graph


def test_owlrl_inverse():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.o, ex.pInverse, ex.s))

    inferred_graph = test_graph.inference("owlrl")

    assert expected_inference in inferred_graph


def test_reasonable_subclass():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.individual, RDF.type, ex.super))

    inferred_graph = test_graph.inference("reasonable")

    assert expected_inference in inferred_graph


def test_reasonable_inverse():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.o, ex.pInverse, ex.s))

    inferred_graph = test_graph.inference("reasonable")

    assert expected_inference in inferred_graph


def test_allegro_subclass():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.individual, RDF.type, ex.super))

    inferred_graph = test_graph.inference("allegro")

    assert expected_inference in inferred_graph


def test_allegro_inverse():
    """Run reasoner and check if expected inference is in the inferred graph."""

    test_graph = get_test_graph()
    expected_inference = ((ex.o, ex.pInverse, ex.s))

    inferred_graph = test_graph.inference("allegro")

    assert expected_inference in inferred_graph
