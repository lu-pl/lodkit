"""Pytest entry point for ClosedOntologyNamespace tests."""

import pytest

from lodkit import ClosedOntologyNamespace, NoSolutionException
from rdflib import Graph, RDF, RDFS, URIRef


def test_closed_ns_term_types():
    """Check if all RDF type terms are recognized by ClosedOntologyNamespace."""

    data = """
    @prefix ex: <http://example.org/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .

    <urn:rdf_class> a rdfs:Class .
    <urn:owl_class> a owl:Class .

    <urn:rdf_property> a rdf:Property .
    <urn:owl_objectproperty> a owl:ObjectProperty .
    <urn:owl_datatypeproperty> a owl:DatatypeProperty .
    <urn:owl_annotationproperty> a owl:AnnotationProperty .

    <urn:owl_namedindividual> a owl:NamedIndividual .
    """

    g = Graph().parse(data=data, format="ttl")
    ns = ClosedOntologyNamespace(source=g)

    expected = {
        "rdf_class": URIRef("urn:rdf_class"),
        "owl_class": URIRef("urn:owl_class"),
        "rdf_property": URIRef("urn:rdf_property"),
        "owl_objectproperty": URIRef("urn:owl_objectproperty"),
        "owl_datatypeproperty": URIRef("urn:owl_datatypeproperty"),
        "owl_annotationproperty": URIRef("urn:owl_annotationproperty"),
        "owl_namedindividual": URIRef("urn:owl_namedindividual"),
    }

    assert ns.mapping == expected


def test_closed_ns_delimited_iris():
    """Check name extraction logic for all supported delimiters."""
    data = """
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

    <foo://example.com:8042/over/there?name=ferret> a rdfs:Class .
    <foo://example.com:8042/over/there?name=ferret#nose> a rdfs:Class .
    <https://example.com#s4> a rdfs:Class .
    <https://example.com/ok/> a rdfs:Class .
    <https://example.com/s3> a rdfs:Class .
    <https://example.com/something#s5> a rdfs:Class .
    <urn:example/s2> a rdfs:Class .
    <urn:s1> a rdfs:Class .
    """
    g = Graph().parse(data=data, format="ttl")
    ns = ClosedOntologyNamespace(source=g)

    expected = {
        "s1": URIRef("urn:s1"),
        "s2": URIRef("urn:example/s2"),
        "s3": URIRef("https://example.com/s3"),
        "s4": URIRef("https://example.com#s4"),
        "s5": URIRef("https://example.com/something#s5"),
        "nose": URIRef("foo://example.com:8042/over/there?name=ferret#nose"),
        "there?name=ferret": URIRef("foo://example.com:8042/over/there?name=ferret"),
    }

    assert ns.mapping == expected

    # getitem checks
    for k, v in ns.mapping.items():
        assert ns[k] == expected[k]


def test_closed_ns_name_collisions():
    """Check handling of collisions between RDF term names and class namespace names.

    In the case of RDF term names conflicting with class namespace names,
    class namespace names take precedence over term names for attribute access.

    Getitem access on ClosedOntologyNamespace directly and ClosedOntologyNamespace.mapping
    retrieve the RDF term however.
    """

    g = Graph()

    triples = [
        (URIRef("urn:mapping"), RDF.type, RDFS.Class),
        (URIRef("urn:source"), RDF.type, RDFS.Class),
    ]

    for triple in triples:
        g.add(triple)

    ns = ClosedOntologyNamespace(source=g)

    expected = {"mapping": URIRef("urn:mapping"), "source": URIRef("urn:source")}

    assert ns.source is g
    assert ns.mapping == expected

    assert ns["mapping"] == URIRef("urn:mapping")
    assert ns["source"] == URIRef("urn:source")


def test_closed_ns_no_solution():
    """Check that NoSolutionException is raised if no classes/properties are found."""

    g = Graph()

    with pytest.raises(NoSolutionException):
        ClosedOntologyNamespace(source=g)


def test_closed_ns_attribute_error():
    """Check that attribute and getitem access failure results in an AttributeError."""

    g = Graph()
    g.add(
        (URIRef("urn:s"), RDF.type, RDFS.Class)
    )  # add a class assertion to avoid NoSolutionException

    ns = ClosedOntologyNamespace(source=g)

    with pytest.raises(AttributeError):
        ns.dne

    with pytest.raises(AttributeError):
        ns["dne"]
