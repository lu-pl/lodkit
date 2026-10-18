"""Pytest entry point for lodkit.literal tests."""

import datetime
import decimal
from fractions import Fraction
from typing import NamedTuple
from xml.dom.minidom import Document

import pytest
from rdflib import Literal
from rdflib.xsd_datetime import Duration

from lodkit import literal


class LiteralTestParameter(NamedTuple):
    obj: object
    expected: Literal
    comment: str = ""


params: list[LiteralTestParameter] = [
    LiteralTestParameter(
        obj=Literal("literal"),
        expected=Literal("literal"),
        comment="An rdflib.Literal is forwarded unchanged.",
    ),
    LiteralTestParameter(
        obj=Literal("1", datatype="http://www.w3.org/2001/XMLSchema#integer"),
        expected=Literal("1", datatype="http://www.w3.org/2001/XMLSchema#integer"),
        comment="A typed rdflib.Literal is forwarded unchanged.",
    ),
    LiteralTestParameter(
        obj="literal",
        expected=Literal("literal"),
        comment="A str object converts to an untyped Literal.",
    ),
    LiteralTestParameter(
        obj=1,
        expected=Literal("1", datatype="http://www.w3.org/2001/XMLSchema#integer"),
        comment="An int object converts to an xsd:integer Literal.",
    ),
    LiteralTestParameter(
        obj=3.14,
        expected=Literal("3.14", datatype="http://www.w3.org/2001/XMLSchema#double"),
        comment="A float object converts to an xsd:double Literal.",
    ),
    LiteralTestParameter(
        obj=True,
        expected=Literal("true", datatype="http://www.w3.org/2001/XMLSchema#boolean"),
        comment="A bool object converts to an xsd:boolean Literal.",
    ),
    LiteralTestParameter(
        obj=decimal.Decimal("1.5"),
        expected=Literal("1.5", datatype="http://www.w3.org/2001/XMLSchema#decimal"),
        comment="A decimal.Decimal object converts to an xsd:decimal Literal.",
    ),
    LiteralTestParameter(
        obj=datetime.date(2024, 1, 1),
        expected=Literal(
            "2024-01-01", datatype="http://www.w3.org/2001/XMLSchema#date"
        ),
        comment="A datetime.date object converts to an xsd:date Literal.",
    ),
    LiteralTestParameter(
        obj=datetime.datetime(2024, 1, 1, 12, 30, 0),
        expected=Literal(
            "2024-01-01T12:30:00",
            datatype="http://www.w3.org/2001/XMLSchema#dateTime",
        ),
        comment="A datetime.datetime object converts to an xsd:dateTime Literal.",
    ),
    LiteralTestParameter(
        obj=datetime.time(12, 30, 0),
        expected=Literal("12:30:00", datatype="http://www.w3.org/2001/XMLSchema#time"),
        comment="A datetime.time object converts to an xsd:time Literal.",
    ),
    LiteralTestParameter(
        obj=datetime.timedelta(days=1),
        expected=Literal(
            "P1D", datatype="http://www.w3.org/2001/XMLSchema#dayTimeDuration"
        ),
        comment="A datetime.timedelta object converts to an xsd:dayTimeDuration Literal.",
    ),
    LiteralTestParameter(
        obj=Duration(days=1, seconds=3600),
        expected=Literal(
            "P1DT1H", datatype="http://www.w3.org/2001/XMLSchema#duration"
        ),
        comment="An rdflib.xsd_datetime.Duration object converts to an xsd:duration Literal.",
    ),
    LiteralTestParameter(
        obj=Document(),
        expected=Literal(
            "",
            datatype="http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral",
        ),
        comment="An xml.dom.minidom.Document object converts to an rdf:XMLLiteral Literal.",
    ),
    LiteralTestParameter(
        obj=Fraction(1, 2),
        expected=Literal("1/2", datatype="http://www.w3.org/2002/07/owl#rational"),
        comment="A fractions.Fraction object converts to an owl:rational Literal.",
    ),
]


@pytest.mark.parametrize("param", params, ids=[param.comment for param in params])
def test_literal(param):
    """Run literal against various object types and compare results against expected literals."""
    assert literal(param.obj) == param.expected


@pytest.mark.parametrize("invalid_object", [None, type("Foo", (), {})(), b"bytes"])
def test_fail_literal(invalid_object):
    """None, an instance of an unrecognized class and bytes must all raise.

    bytes is a deliberate negative case, not an oversight: it is excluded
    from lodkit.types.TypedLiteral even though rdflib.Literal round-trips
    it in the opposite direction (see TypedLiteral's docstring), and
    literal's object coercion is enforced against exactly that union.
    """
    with pytest.raises(ValueError):
        literal(invalid_object)
