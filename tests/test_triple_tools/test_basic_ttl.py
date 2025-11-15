"""Pytest entry point for basic lodkit.ttl tests."""

from typing import NamedTuple

import pytest
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import isomorphic

from lodkit import _TripleObject, _TripleSubject, ttl
from lodkit.triple_tools.ttl_constructor import _TPredicateObjectPair


class TestParameter(NamedTuple):
    s: _TripleSubject
    po: list[_TPredicateObjectPair]
    expected: list[tuple[_TripleSubject, URIRef, _TripleObject]]
    comment: str | None = None


params: list[TestParameter] = [
    # literal object
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), Literal("literal"))],
        expected=[(URIRef("urn:s"), URIRef("urn:p"), Literal("literal"))],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:p2"), Literal("literal")),
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p2"), Literal("literal")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), "literal")],
        expected=[(URIRef("urn:s"), URIRef("urn:p"), Literal("literal"))],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), "literal"), (URIRef("urn:p"), "literal 2")],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal 2")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), "literal"), (URIRef("urn:p"), Literal("literal 2"))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal 2")),
        ],
        comment="Mixing str | rdflib.Literal",
    ),
    # URI object
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), URIRef("urn:o"))],
        expected=[(URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o"))],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), URIRef("urn:o")), (URIRef("urn:p2"), URIRef("urn:o"))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
            (URIRef("urn:s"), URIRef("urn:p2"), URIRef("urn:o")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), URIRef("urn:o")), (URIRef("urn:p"), Literal("literal"))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
        ],
        comment="Mixing URI and Literal object.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), URIRef("urn:o")), (URIRef("urn:p"), "literal")],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
        ],
        comment="Mixing URI and Literal object with str argument.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), (URIRef("urn:o"), URIRef("urn:o2")))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o2")),
        ],
        comment="Object list notation with URIs.",
    ),
    # object lists
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), (Literal("literal"), "literal 2"))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal 2")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), (Literal("literal"), URIRef("urn:o")))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), ("literal", URIRef("urn:o")))],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:o")),
        ],
    ),
    # ttl objects
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                ttl(URIRef("urn:s2"), (URIRef("urn:p2"), Literal("literal"))),
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:s2")),
            (URIRef("urn:s2"), URIRef("urn:p2"), Literal("literal")),
        ],
        comment="Basic ttl object.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (URIRef("urn:p"), Literal("literal")),
            (
                URIRef("urn:p"),
                ttl(URIRef("urn:s2"), (URIRef("urn:p2"), Literal("literal"))),
            ),
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:s2")),
            (URIRef("urn:s2"), URIRef("urn:p2"), Literal("literal")),
        ],
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                ttl(
                    URIRef("urn:s2"),
                    (URIRef("urn:p2"), Literal("literal")),
                    (URIRef("urn:p2"), Literal("literal 2")),
                ),
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:s2")),
            (URIRef("urn:s2"), URIRef("urn:p2"), Literal("literal")),
            (URIRef("urn:s2"), URIRef("urn:p2"), Literal("literal 2")),
        ],
        comment="Basic ttl object with second predicate.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                ttl(
                    URIRef("urn:s2"),
                    (
                        URIRef("urn:p2"),
                        ttl(URIRef("urn:s3"), (URIRef("urn:p3"), "literal")),
                    ),
                ),
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:s2")),
            (URIRef("urn:s2"), URIRef("urn:p2"), URIRef("urn:s3")),
            (URIRef("urn:s3"), URIRef("urn:p3"), Literal("literal")),
        ],
        comment="Double nested ttl.",
    ),
]


bnode1, bnode2, bnode3 = BNode(), BNode(), BNode()
bnode_params = [
    TestParameter(
        s=URIRef("urn:s"),
        po=[(URIRef("urn:p"), [(URIRef("urn:p2"), Literal("literal"))])],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), Literal("literal")),
        ],
        comment="Basic BNode object.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                [
                    (URIRef("urn:p2"), Literal("literal")),
                    (URIRef("urn:p3"), Literal("literal")),
                ],
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), Literal("literal")),
            (bnode1, URIRef("urn:p3"), Literal("literal")),
        ],
        comment="Multiple BNode object assertions.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                [(URIRef("urn:p2"), [(URIRef("urn:p3"), Literal("literal"))])],
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), bnode2),
            (bnode2, URIRef("urn:p3"), Literal("literal")),
        ],
        comment="Nested BNode object assertions.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                [
                    (
                        URIRef("urn:p2"),
                        [
                            (URIRef("urn:p3"), Literal("literal")),
                            (URIRef("urn:p4"), Literal("literal")),
                        ],
                    )
                ],
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), bnode2),
            (bnode2, URIRef("urn:p3"), Literal("literal")),
            (bnode2, URIRef("urn:p4"), Literal("literal")),
        ],
        comment="Nested BNode object with multi assertions.",
    ),
    # bnode objects iterators
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                iter(
                    [
                        (
                            URIRef("urn:p2"),
                            iter(
                                [
                                    (URIRef("urn:p3"), Literal("literal")),
                                    (URIRef("urn:p4"), Literal("literal")),
                                ]
                            ),
                        )
                    ]
                ),
            )
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), bnode2),
            (bnode2, URIRef("urn:p3"), Literal("literal")),
            (bnode2, URIRef("urn:p4"), Literal("literal")),
        ],
        comment="Nested BNode object with multi assertions; but with iterators.",
    ),
    # object list recursion
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                (
                    "literal",
                    [(URIRef("urn:p2"), "literal 2")],
                    ttl(
                        URIRef("urn:s2"),
                        (URIRef("urn:p3"), "literal 3"),
                    ),
                ),
            ),
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (URIRef("urn:s"), URIRef("urn:p"), URIRef("urn:s2")),
            (bnode1, URIRef("urn:p2"), Literal("literal 2")),
            (URIRef("urn:s2"), URIRef("urn:p3"), Literal("literal 3")),
        ],
        comment="Constructor with literal, bnode and ttl elements in an object list.",
    ),
    TestParameter(
        s=URIRef("urn:s"),
        po=[
            (
                URIRef("urn:p"),
                (
                    "literal",
                    [
                        (URIRef("urn:p2"), "literal 2"),
                        (
                            URIRef("urn:p3"),
                            ttl(
                                URIRef("urn:s2"),
                                (URIRef("urn:p4"), "literal 3"),
                            ),
                        ),
                    ],
                ),
            ),
        ],
        expected=[
            (URIRef("urn:s"), URIRef("urn:p"), Literal("literal")),
            (URIRef("urn:s"), URIRef("urn:p"), bnode1),
            (bnode1, URIRef("urn:p2"), Literal("literal 2")),
            (bnode1, URIRef("urn:p3"), URIRef("urn:s2")),
            (URIRef("urn:s2"), URIRef("urn:p4"), Literal("literal 3")),
        ],
        comment="Constructor with literal and blank node with nested ttl in an object list.",
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
