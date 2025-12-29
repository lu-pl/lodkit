"""Pytest entry point for basic lodkit.ttl tests."""

from typing import NamedTuple

import pytest
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef
from rdflib.compare import isomorphic

from lodkit import ttl
from lodkit.triple_tools.ttl_constructor import TPredicateObjectPair
from lodkit.types import TripleObject, TripleSubject


class TripleConstructorTestParameter(NamedTuple):
    s: TripleSubject
    po: list[TPredicateObjectPair]
    expected: list[tuple[TripleSubject, URIRef, TripleObject]]
    comment: str | None = None


ex = Namespace("https://example.com")


params: list[TripleConstructorTestParameter] = [
    # literal object
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, Literal("literal"))],
        expected=[(ex.s, ex.p, Literal("literal"))],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (ex.p, Literal("literal")),
            (ex.p2, Literal("literal")),
        ],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p2, Literal("literal")),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, "literal")],
        expected=[(ex.s, ex.p, Literal("literal"))],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, "literal"), (ex.p, "literal 2")],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, Literal("literal 2")),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, "literal"), (ex.p, Literal("literal 2"))],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, Literal("literal 2")),
        ],
        comment="Mixing str | rdflib.Literal",
    ),
    # URI object
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ex.o)],
        expected=[(ex.s, ex.p, ex.o)],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ex.o), (ex.p2, ex.o)],
        expected=[
            (ex.s, ex.p, ex.o),
            (ex.s, ex.p2, ex.o),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ex.o), (ex.p, Literal("literal"))],
        expected=[
            (ex.s, ex.p, ex.o),
            (ex.s, ex.p, Literal("literal")),
        ],
        comment="Mixing URI and Literal object.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ex.o), (ex.p, "literal")],
        expected=[
            (ex.s, ex.p, ex.o),
            (ex.s, ex.p, Literal("literal")),
        ],
        comment="Mixing URI and Literal object with str argument.",
    ),
    # object list notation
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ex.o, ex.o2)],
        expected=[
            (ex.s, ex.p, ex.o),
            (ex.s, ex.p, ex.o2),
        ],
        comment="Object list notation with URIs.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, "literal", "literal 2")],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, Literal("literal 2")),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, Literal("literal"), ex.o)],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, ex.o),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, "literal", ex.o)],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, ex.o),
        ],
    ),
    # ttl objects
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                ttl(ex.s2, (ex.p2, Literal("literal"))),
            )
        ],
        expected=[
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p2, Literal("literal")),
        ],
        comment="Basic ttl object.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (ex.p, Literal("literal")),
            (
                ex.p,
                ttl(ex.s2, (ex.p2, Literal("literal"))),
            ),
        ],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p2, Literal("literal")),
        ],
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                ttl(
                    ex.s2,
                    (ex.p2, Literal("literal")),
                    (ex.p2, Literal("literal 2")),
                ),
            )
        ],
        expected=[
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p2, Literal("literal")),
            (ex.s2, ex.p2, Literal("literal 2")),
        ],
        comment="Basic ttl object with second predicate.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                ttl(
                    ex.s2,
                    (
                        ex.p2,
                        ttl(ex.s3, (ex.p3, "literal")),
                    ),
                ),
            )
        ],
        expected=[
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p2, ex.s3),
            (ex.s3, ex.p3, Literal("literal")),
        ],
        comment="Double nested ttl.",
    ),
]


## ttl code paths that generate blank nodes cannot be tested by simple tuple comparison;
## the tests below use global bnodes, loads asserted and expected triples into a graph and test for isomorphy.
bnode1, bnode2, bnode3, bnode4, bnode5, bnode6 = (
    BNode(),
    BNode(),
    BNode(),
    BNode(),
    BNode(),
    BNode(),
)
bnode_params = [
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, [(ex.p2, Literal("literal"))])],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, Literal("literal")),
        ],
        comment="Basic BNode object.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                [
                    (ex.p2, Literal("literal")),
                    (ex.p3, Literal("literal")),
                ],
            )
        ],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, Literal("literal")),
            (bnode1, ex.p3, Literal("literal")),
        ],
        comment="Multiple BNode object assertions.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                [(ex.p2, [(ex.p3, Literal("literal"))])],
            )
        ],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, bnode2),
            (bnode2, ex.p3, Literal("literal")),
        ],
        comment="Nested BNode object assertions.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                [
                    (
                        ex.p2,
                        [
                            (ex.p3, Literal("literal")),
                            (ex.p4, Literal("literal")),
                        ],
                    )
                ],
            )
        ],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, bnode2),
            (bnode2, ex.p3, Literal("literal")),
            (bnode2, ex.p4, Literal("literal")),
        ],
        comment="Nested BNode object with multi assertions.",
    ),
    # object list recursion
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                "literal",
                [(ex.p2, "literal 2")],
                ttl(
                    ex.s2,
                    (ex.p3, "literal 3"),
                ),
            ),
        ],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, Literal("literal 2")),
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p3, Literal("literal 3")),
        ],
        comment="Constructor with literal, bnode and ttl elements in an object list.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                "literal",
                [
                    (ex.p2, "literal 2"),
                    (
                        ex.p3,
                        ttl(
                            ex.s2,
                            (ex.p4, "literal 3"),
                        ),
                    ),
                ],
            ),
        ],
        expected=[
            (ex.s, ex.p, Literal("literal")),
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, Literal("literal 2")),
            (bnode1, ex.p3, ex.s2),
            (ex.s2, ex.p4, Literal("literal 3")),
        ],
        comment="Constructor with literal and blank node with nested ttl in an object list.",
    ),
    # RDF collection tests
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, (ex.o,))],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, RDF.first, ex.o),
            (bnode1, RDF.rest, RDF.nil),
        ],
        comment="Simple RDF Collection with a single element collection.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, (ex.o))],
        expected=[(ex.s, ex.p, ex.o)],
        comment="Note that the object it NOT a single element tuple!",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, (ex.o1, ex.o2))],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, RDF.first, ex.o1),
            (bnode1, RDF.rest, bnode2),
            (bnode2, RDF.first, ex.o2),
            (bnode2, RDF.rest, RDF.nil),
        ],
        comment="Simple RDF Collection with a two element collection.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, (ex.o1, ex.o2, "literal"))],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, RDF.first, ex.o1),
            (bnode1, RDF.rest, bnode2),
            (bnode2, RDF.first, ex.o2),
            (bnode2, RDF.rest, bnode3),
            (bnode3, RDF.first, Literal("literal")),
            (bnode3, RDF.rest, RDF.nil),
        ],
        comment="Simple RDF Collection with a three element collection.",
    ),
    ## recursive code paths
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ttl(ex.s2, (ex.p2, "1")), [(ex.p3, "2")], ("3",))],
        expected=[
            (ex.s, ex.p, ex.s2),
            (ex.s2, ex.p2, Literal("1")),
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p3, Literal("2")),
            (ex.s, ex.p, bnode2),
            (bnode2, RDF.first, Literal("3")),
            (bnode2, RDF.rest, RDF.nil),
        ],
        comment="Recursive object list.",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[
            (
                ex.p,
                [
                    (ex.p2, "1"),
                    (ex.p3, ("2",)),
                    (ex.p4, ttl(ex.s2, (ex.p5, "3"))),
                    (ex.p6, [(ex.p7, "4")]),
                ],
            )
        ],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, ex.p2, Literal("1")),
            (bnode1, ex.p3, bnode2),
            (bnode2, RDF.first, Literal("2")),
            (bnode2, RDF.rest, RDF.nil),
            (bnode1, ex.p4, ex.s2),
            (ex.s2, ex.p5, Literal("3")),
            (bnode1, ex.p6, bnode3),
            (bnode3, ex.p7, Literal("4")),
        ],
        comment="recursive blank node",
    ),
    TripleConstructorTestParameter(
        s=ex.s,
        po=[(ex.p, ("1", ttl(ex.s2, (ex.p2, ex.o, "2")), [(ex.p3, "3")], ("4",)))],
        expected=[
            (ex.s, ex.p, bnode1),
            (bnode1, RDF.first, Literal("1")),
            (bnode1, RDF.rest, bnode2),
            (bnode2, RDF.first, ex.s2),
            (ex.s2, ex.p2, ex.o),
            (ex.s2, ex.p2, Literal("2")),
            (bnode2, RDF.rest, bnode3),
            (bnode3, RDF.first, bnode4),
            (bnode4, ex.p3, Literal("3")),
            (bnode3, RDF.rest, bnode5),
            (bnode5, RDF.first, bnode6),
            (bnode6, RDF.first, Literal("4")),
            (bnode6, RDF.rest, RDF.nil),
            (bnode5, RDF.rest, RDF.nil),
        ],
        comment="Recursive collection.",
    ),
]


@pytest.mark.parametrize("param", params)
def test_iterator_ttl(param):
    """Simply compare generated against expected triples."""
    triples = ttl(param.s, *param.po)
    assert list(triples) == param.expected


@pytest.mark.parametrize("param", bnode_params)
def test_bnode_ttl(param):
    """Construct a graph from generated and expected triples and check for isomorphy."""
    result_graph: Graph = ttl(param.s, *param.po).to_graph()
    expected_graph: Graph = Graph()

    for triple in param.expected:
        expected_graph.add(triple)

    assert isomorphic(result_graph, expected_graph)


@pytest.mark.parametrize("invalid_object", [1, None, type("Foo", (), {})])
def test_fail_ttl(invalid_object):
    with pytest.raises(TypeError):
        list(ttl(URIRef("urn:s"), (URIRef("urn:p"), invalid_object)))
