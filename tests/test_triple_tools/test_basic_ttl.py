"""Pytest entry point for basic lodkit.ttl tests."""

import datetime
import decimal
from fractions import Fraction
from typing import NamedTuple
from xml.dom.minidom import Document

import pytest
from inline_snapshot import snapshot
from rdflib import BNode, Literal, Namespace, URIRef
from rdflib.xsd_datetime import Duration

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
    # Python object -> typed Literal conversion
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, 1)),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "1"^^<http://www.w3.org/2001/XMLSchema#integer> .'
            ]
        ),
        comment="int object converts to an xsd:integer Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, 3.14)),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "3.14"^^<http://www.w3.org/2001/XMLSchema#double> .'
            ]
        ),
        comment="float object converts to an xsd:double Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, True)),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "true"^^<http://www.w3.org/2001/XMLSchema#boolean> .'
            ]
        ),
        comment="bool object converts to an xsd:boolean Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, decimal.Decimal("1.5"))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "1.5"^^<http://www.w3.org/2001/XMLSchema#decimal> .'
            ]
        ),
        comment="decimal.Decimal object converts to an xsd:decimal Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, datetime.date(2024, 1, 1))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "2024-01-01"^^<http://www.w3.org/2001/XMLSchema#date> .'
            ]
        ),
        comment="datetime.date object converts to an xsd:date Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, datetime.datetime(2024, 1, 1, 12, 30, 0))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "2024-01-01T12:30:00"^^<http://www.w3.org/2001/XMLSchema#dateTime> .'
            ]
        ),
        comment="datetime.datetime object converts to an xsd:dateTime Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, datetime.time(12, 30, 0))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "12:30:00"^^<http://www.w3.org/2001/XMLSchema#time> .'
            ]
        ),
        comment="datetime.time object converts to an xsd:time Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, datetime.timedelta(days=1))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "P1D"^^<http://www.w3.org/2001/XMLSchema#dayTimeDuration> .'
            ]
        ),
        comment="datetime.timedelta object converts to an xsd:dayTimeDuration Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, Duration(days=1, seconds=3600))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "P1DT1H"^^<http://www.w3.org/2001/XMLSchema#duration> .'
            ]
        ),
        comment="rdflib.xsd_datetime.Duration object converts to an xsd:duration Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, Document())),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> ""^^<http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> .'
            ]
        ),
        comment="xml.dom.minidom.Document object converts to an rdf:XMLLiteral Literal.",
    ),
    TripleConstructorTestParameter(
        ttl_obj=ttl(ex.s, (ex.p, Fraction(1, 2))),
        expected=snapshot(
            [
                '<https://example.coms> <https://example.comp> "1/2"^^<http://www.w3.org/2002/07/owl#rational> .'
            ]
        ),
        comment=(
            "fractions.Fraction object converts to an owl:rational Literal. "
            "Note this does not round-trip generically via .toPython() - see "
            "lodkit.types.TypedLiteral's docstring - but that is out of scope "
            "for ttl's object coercion, which is an encode-only concern."
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


@pytest.mark.parametrize("invalid_object", [None, type("Foo", (), {}), b"bytes"])
def test_fail_ttl(invalid_object):
    """None, an unrecognized class and bytes must all raise.

    bytes is a deliberate negative case, not an oversight: it is excluded
    from lodkit.types.TypedLiteral even though rdflib.Literal round-trips
    it in the opposite direction (see TypedLiteral's docstring), and ttl's
    object coercion is enforced against exactly that union.
    """
    with pytest.raises(ValueError):
        list(ttl(URIRef("urn:s"), (URIRef("urn:p"), invalid_object)))


def test_fail_ttl_single_element_pair():
    """A predicate-object pair without an object must raise, not silently yield nothing."""
    with pytest.raises(ValueError):
        list(ttl(URIRef("urn:s"), (URIRef("urn:p"),)))


# The following subject factory tests compare for len instead of a canonicalized snapshot
# because the nodes of interest are structurally and thus canonically equal;
# canonicalization resolves the structural tie-break by assigning generated nodes;
# a snapshot would thus record dynamic and arbitrary values.


def test_ttl_empty_list_subject_fresh_per_iteration():
    """ttl([], ...) must generate a fresh BNode on every separate consumption.

    Regression test for #74: the blank node used to be generated once in
    __init__ and reused for the lifetime of the ttl instance. Two separately
    generated graphs union to two distinct triples rather than deduplicating
    to one, since each to_graph() call gets its own fresh blank node.
    """
    triples = ttl([], (ex.p, ex.o))
    graph = triples.to_graph() + triples.to_graph()
    assert len(graph) == 2


def test_ttl_subject_factory():
    """A zero-argument callable subject (here: the bare BNode class) is called fresh each access.

    BNode itself is a valid factory simply because classes are callable;
    calling it constructs a new instance, exactly like any other factory.
    """
    triples = ttl(BNode, (ex.p, ex.o))
    graph = triples.to_graph() + triples.to_graph()
    assert len(graph) == 2


def test_ttl_fixed_bnode_instance_subject_is_stable():
    """A concrete BNode() instance (as opposed to the BNode class) is a fixed, non-factory subject.

    Contrasts with test_ttl_subject_factory: two separately generated graphs
    union to a single triple, since both use the exact same subject.
    """
    triples = ttl(BNode(), (ex.p, ex.o))
    graph = triples.to_graph() + triples.to_graph()
    assert len(graph) == 1


def test_ttl_subject_setter():
    """Reassigning .subject after construction changes the resolved subject."""
    triples = ttl(ex.s1, (ex.p, ex.o))
    triples.subject = ex.s2

    (subject, _, _), *_ = list(triples)
    assert subject == ex.s2


def test_ttl_nested_object_factory_subject_consistency():
    """A nested ttl object with a factory subject must use one resolved value consistently.

    The subject factory is resolved once per use; the link triple to the
    nested object and the nested object's own triples must agree on the
    same concrete subject rather than each independently re-invoking the
    factory (which would produce two different, mismatched blank nodes).
    """
    inner = ttl(BNode, (ex.p2, Literal("x")))
    outer = ttl(ex.s, (ex.p, inner))

    triples = list(outer)
    link_object = next(o for _, p, o in triples if p == ex.p)
    nested_subject = next(s for s, p, _ in triples if p == ex.p2)

    assert link_object == nested_subject


@pytest.mark.parametrize("invalid_subject", [None, "not a subject", 1])
def test_fail_ttl_invalid_subject(invalid_subject):
    """A subject that is neither a TripleSubject, a factory, nor [] must raise ValueError."""
    with pytest.raises(ValueError):
        list(ttl(invalid_subject, (ex.p, ex.o)))
