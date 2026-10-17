"""Pytest entry point for basic lodkit.ttl tests."""

from typing import NamedTuple

import pytest
from inline_snapshot import snapshot
from rdflib import Literal, Namespace, URIRef

from lodkit import ttl
from tests.test_triple_tools.helpers import canonical_triples


class TripleConstructorTestParameter(NamedTuple):
    ttl_obj: ttl
    expected: list[str]
    comment: str | None = None


ex = Namespace("https://example.com")


params: list[TripleConstructorTestParameter] = [
    # literal object
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, Literal("literal"))),
        expected=snapshot(
            ['<https://example.coms> <https://example.comp> "literal" .']
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (ex.p, Literal("literal")),
            (ex.p2, Literal("literal")),
        ),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp2> "literal" .',
                '<https://example.coms> <https://example.comp> "literal" .',
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, "literal")),
        expected=snapshot(
            ['<https://example.coms> <https://example.comp> "literal" .']
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, "literal"), (ex.p, "literal 2")),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal 2" .',
                '<https://example.coms> <https://example.comp> "literal" .',
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, "literal"), (ex.p, Literal("literal 2"))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal 2" .',
                '<https://example.coms> <https://example.comp> "literal" .',
            ]
        ),
        comment="Mixing str | rdflib.Literal",
    ),
    # URI object
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ex.o)),
        expected=snapshot(
            ["<https://example.coms> <https://example.comp> <https://example.como> ."]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ex.o), (ex.p2, ex.o)),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp2> <https://example.como> .",
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ex.o), (ex.p, Literal("literal"))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
        comment="Mixing URI and Literal object.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ex.o), (ex.p, "literal")),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
        comment="Mixing URI and Literal object with str argument.",
    ),
    # object list notation
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ex.o, ex.o2)),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> <https://example.como2> .",
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
        comment="Object list notation with URIs.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, "literal", "literal 2")),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal 2" .',
                '<https://example.coms> <https://example.comp> "literal" .',
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, Literal("literal"), ex.o)),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, "literal", ex.o)),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.como> .",
            ]
        ),
    ),
    # ttl objects
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                ttl(ex.s2, (ex.p2, Literal("literal"))),
            ),
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp2> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
            ]
        ),
        comment="Basic ttl object.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (ex.p, Literal("literal")),
            (
                ex.p,
                ttl(ex.s2, (ex.p2, Literal("literal"))),
            ),
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp2> "literal" .',
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
            ]
        ),
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                ttl(
                    ex.s2,
                    (ex.p2, Literal("literal")),
                    (ex.p2, Literal("literal 2")),
                ),
            ),
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp2> "literal 2" .',
                '<https://example.coms2> <https://example.comp2> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
            ]
        ),
        comment="Basic ttl object with second predicate.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                ttl(
                    ex.s2,
                    (
                        ex.p2,
                        ttl(ex.s3, (ex.p3, "literal")),
                    ),
                ),
            ),
        ),
        expected=snapshot(
            [
                "<https://example.coms2> <https://example.comp2> <https://example.coms3> .",
                '<https://example.coms3> <https://example.comp3> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
            ]
        ),
        comment="Double nested ttl.",
    ),
    # BNode objects
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, [(ex.p2, Literal("literal"))])),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                '_:cb0 <https://example.comp2> "literal" .',
            ]
        ),
        comment="Basic BNode object.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                [
                    (ex.p2, Literal("literal")),
                    (ex.p3, Literal("literal")),
                ],
            ),
        ),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                '_:cb0 <https://example.comp2> "literal" .',
                '_:cb0 <https://example.comp3> "literal" .',
            ]
        ),
        comment="Multiple BNode object assertions.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                [(ex.p2, [(ex.p3, Literal("literal"))])],
            ),
        ),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                "_:cb0 <https://example.comp2> _:cb6eb201c1d0abe7ff45c151b27270b816ca50e781904eda65cdce92d95352aebe .",
                '_:cb6eb201c1d0abe7ff45c151b27270b816ca50e781904eda65cdce92d95352aebe <https://example.comp3> "literal" .',
            ]
        ),
        comment="Nested BNode object assertions.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
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
            ),
        ),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                "_:cb0 <https://example.comp2> _:cbc2a69c9a07ca53d5a31c09893c9045b2974fb6295bd0230486e5cebc86b67524 .",
                '_:cbc2a69c9a07ca53d5a31c09893c9045b2974fb6295bd0230486e5cebc86b67524 <https://example.comp3> "literal" .',
                '_:cbc2a69c9a07ca53d5a31c09893c9045b2974fb6295bd0230486e5cebc86b67524 <https://example.comp4> "literal" .',
            ]
        ),
        comment="Nested BNode object with multi assertions.",
    ),
    # object list recursion
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                "literal",
                [(ex.p2, "literal 2")],
                ttl(
                    ex.s2,
                    (ex.p3, "literal 3"),
                ),
            ),
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp3> "literal 3" .',
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
                "<https://example.coms> <https://example.comp> _:cb0 .",
                '_:cb0 <https://example.comp2> "literal 2" .',
            ]
        ),
        comment="Constructor with literal, bnode and ttl elements in an object list.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
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
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp4> "literal 3" .',
                '<https://example.coms> <https://example.comp> "literal" .',
                "<https://example.coms> <https://example.comp> _:cb0 .",
                '_:cb0 <https://example.comp2> "literal 2" .',
                "_:cb0 <https://example.comp3> <https://example.coms2> .",
            ]
        ),
        comment="Constructor with literal and blank node with nested ttl in an object list.",
    ),
    # RDF collection tests
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, (ex.o,))),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.como> .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
            ]
        ),
        comment="Simple RDF Collection with a single element collection.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, (ex.o))),
        expected=snapshot(
            ["<https://example.coms> <https://example.comp> <https://example.como> ."]
        ),
        comment="Note that the object it NOT a single element tuple!",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, (ex.o1, ex.o2))),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb0 .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.como1> .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 .",
                "_:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.como2> .",
                "_:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
            ]
        ),
        comment="Simple RDF Collection with a two element collection.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, (ex.o1, ex.o2, "literal"))),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> _:cb3f8bdae2e6c91f0b43c0d33b674b8e6b27985ed298661790696da619a72c0fbd .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.como2> .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cb10c3439f5ee75ada7f286418878ab98a3860279b3b01e985112df1961f20f2973 .",
                '_:cb10c3439f5ee75ada7f286418878ab98a3860279b3b01e985112df1961f20f2973 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "literal" .',
                "_:cb10c3439f5ee75ada7f286418878ab98a3860279b3b01e985112df1961f20f2973 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
                "_:cb3f8bdae2e6c91f0b43c0d33b674b8e6b27985ed298661790696da619a72c0fbd <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.como1> .",
                "_:cb3f8bdae2e6c91f0b43c0d33b674b8e6b27985ed298661790696da619a72c0fbd <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cb0 .",
            ]
        ),
        comment="Simple RDF Collection with a three element collection.",
    ),
    ## recursive code paths
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ttl(ex.s2, (ex.p2, "1")), [(ex.p3, "2")], ("3",))),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp2> "1" .',
                "<https://example.coms> <https://example.comp> <https://example.coms2> .",
                "<https://example.coms> <https://example.comp> _:cb0 .",
                "<https://example.coms> <https://example.comp> _:cba6ac028120a834ce8d5972f1e79870092505e60945d1dfcdadcacf6d3da4c7c .",
                '_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "3" .',
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
                '_:cba6ac028120a834ce8d5972f1e79870092505e60945d1dfcdadcacf6d3da4c7c <https://example.comp3> "2" .',
            ]
        ),
        comment="Recursive object list.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s,
            (
                ex.p,
                [
                    (ex.p2, "1"),
                    (ex.p3, ("2",)),
                    (ex.p4, ttl(ex.s2, (ex.p5, "3"))),
                    (ex.p6, [(ex.p7, "4")]),
                ],
            ),
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp5> "3" .',
                "<https://example.coms> <https://example.comp> _:cb878e2b9cb02b3d85ee4cd3c1e93240f5e7a60397446b753a9b7d28507e3781c2 .",
                '_:cb0 <https://example.comp7> "4" .',
                '_:cb1402214540a6a4172952879f53819326b4a89598a419c0862379d766ad589feb <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "2" .',
                "_:cb1402214540a6a4172952879f53819326b4a89598a419c0862379d766ad589feb <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
                '_:cb878e2b9cb02b3d85ee4cd3c1e93240f5e7a60397446b753a9b7d28507e3781c2 <https://example.comp2> "1" .',
                "_:cb878e2b9cb02b3d85ee4cd3c1e93240f5e7a60397446b753a9b7d28507e3781c2 <https://example.comp3> _:cb1402214540a6a4172952879f53819326b4a89598a419c0862379d766ad589feb .",
                "_:cb878e2b9cb02b3d85ee4cd3c1e93240f5e7a60397446b753a9b7d28507e3781c2 <https://example.comp4> <https://example.coms2> .",
                "_:cb878e2b9cb02b3d85ee4cd3c1e93240f5e7a60397446b753a9b7d28507e3781c2 <https://example.comp6> _:cb0 .",
            ]
        ),
        comment="recursive blank node",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(
            ex.s, (ex.p, ("1", ttl(ex.s2, (ex.p2, ex.o, "2")), [(ex.p3, "3")], ("4",)))
        ),
        expected=snapshot(
            [
                '<https://example.coms2> <https://example.comp2> "2" .',
                "<https://example.coms2> <https://example.comp2> <https://example.como> .",
                "<https://example.coms> <https://example.comp> _:cb785c4127b199e48a1ea02452fda1d4edf0f2fadc42d4fc21be113d7a22555a66 .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> _:cb4b251bcea4bd991120627152d1ee12a825a7f9e0cf315edc41cfaa0cf8d53a27 .",
                "_:cb0 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 .",
                '_:cb1231c68fa90abb2798a32dc0ba833902294943140d765888502c8f1a253b7ae56 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "4" .',
                "_:cb1231c68fa90abb2798a32dc0ba833902294943140d765888502c8f1a253b7ae56 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
                '_:cb4b251bcea4bd991120627152d1ee12a825a7f9e0cf315edc41cfaa0cf8d53a27 <https://example.comp3> "3" .',
                '_:cb785c4127b199e48a1ea02452fda1d4edf0f2fadc42d4fc21be113d7a22555a66 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> "1" .',
                "_:cb785c4127b199e48a1ea02452fda1d4edf0f2fadc42d4fc21be113d7a22555a66 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cbef035d9bac124266aca53d618e116a19d3922a2c4cf9818dfa3b1f762dcad963 .",
                "_:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> _:cb1231c68fa90abb2798a32dc0ba833902294943140d765888502c8f1a253b7ae56 .",
                "_:cbd7c96744b860be374134b6eeace4a6009e3d5947219e59b3c009836ad1012775 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> .",
                "_:cbef035d9bac124266aca53d618e116a19d3922a2c4cf9818dfa3b1f762dcad963 <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <https://example.coms2> .",
                "_:cbef035d9bac124266aca53d618e116a19d3922a2c4cf9818dfa3b1f762dcad963 <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> _:cb0 .",
            ]
        ),
        comment="Recursive collection.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, ())),
        expected=snapshot(
            [
                "<https://example.coms> <https://example.comp> <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> ."
            ]
        ),
    ),
]


@pytest.mark.parametrize("param", params)
def test_ttl_triples(param):
    """Compare the canonicalized triples generated by ttl against a snapshot.

    Canonicalization makes blank node labels deterministic, so a single
    comparison style works for triples with and without blank nodes alike.
    """
    graph = param.ttl_obj.to_graph()
    assert canonical_triples(graph) == param.expected


@pytest.mark.parametrize("invalid_object", [1, None, type("Foo", (), {})])
def test_fail_ttl(invalid_object):
    with pytest.raises(TypeError):
        list(ttl(URIRef("urn:s"), (URIRef("urn:p"), invalid_object)))
