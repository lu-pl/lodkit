"""A collection of useful types for working with LOD."""

import datetime
import decimal
from typing import Literal as TLiteral
from xml.dom.minidom import Document

from rdflib import BNode, Literal, URIRef
from rdflib.compat import long_type
from rdflib.xsd_datetime import Duration


__all__ = (
    "TripleSubject",
    "TriplePredicate",
    "RDFTerm",
    "TripleObject",
    "Triple",
    "LiteralObjectTriple",
    "URIObjectTriple",
    "BNodeObjectTriple",
    "GraphParseFormatOptions",
    "TripleParseFormatOptions",
    "QuadParseFormatOptions",
    "GraphSerializeFormatOptions",
    "TripleSerializeFormatOptions",
    "QuadSerializeFormatOptions",
)

type TripleSubject = URIRef | BNode
type TriplePredicate = URIRef
type RDFTerm = Literal | URIRef | BNode
type TripleObject = RDFTerm
type Triple = tuple[TripleSubject, URIRef, TripleObject]

type LiteralObjectTriple = tuple[TripleSubject, URIRef, Literal]
type URIObjectTriple = tuple[TripleSubject, URIRef, URIRef]
type BNodeObjectTriple = tuple[TripleSubject, URIRef, BNode]

type LiteralToPython = (
    Literal
    | None
    | datetime.date
    | datetime.datetime
    | datetime.time
    | datetime.timedelta
    | Duration
    | bytes
    | bool
    | int
    | float
    | decimal.Decimal
    | long_type
    | Document
)
"""Return type for rdflib.Literal.toPython.

This union type represents all possible return value types of Literal.toPython.
Return type provenance:

    - Literal: rdflib.Literal.toPython
    - None: rdflib.term._castLexicalToPython

    - datetime.datetime: rdflib.xsd_datetime.parse_datetime
    - datetime.time: rdflib.xsd_datetime.parse_time
    - datetime.timedelta, Duration: parse_xsd_duration
    - bytes: rdflib.term._unhexlify, base64.b64decode
    - bool: rdflib.term._parseBoolean
    - int, float, decimal.Decimal, long_type: rdflib.term.XSDToPython
    - Document: rdflib.term._parseXML
"""

type GraphParseFormatOptions = TLiteral[
    "application/rdf+xml",
    "xml",
    "text/n3",
    "n3",
    "text/turtle",
    "turtle",
    "ttl",
    "application/n-triples",
    "ntriples",
    "nt",
    "nt11",
    "application/ld+json",
    "json-ld",
    "application/n-quads",
    "nquads",
    "application/trix",
    "trix",
    "application/trig",
    "trig",
    "hext",
]

type TripleParseFormatOptions = TLiteral[
    "application/rdf+xml",
    "xml",
    "text/n3",
    "n3",
    "text/turtle",
    "turtle",
    "ttl",
    "application/n-triples",
    "ntriples",
    "nt",
    "nt11",
    "application/ld+json",
    "json-ld",
    "hext",
]

type QuadParseFormatOptions = TLiteral[
    "nquads",
    "application/n-quads",
    "trix",
    "application/trix",
    "trig",
    "application/trig",
]

type GraphSerializeFormatOptions = TLiteral[
    "application/rdf+xml",
    "xml",
    "pretty-xml",
    "text/n3",
    "n3",
    "text/turtle",
    "turtle",
    "ttl",
    "longturtle",
    "application/n-triples",
    "ntriples",
    "nt",
    "nt11",
    "json-ld",
    "application/ld+json",
    "application/n-quads",
    "nquads",
    "application/trix",
    "trix",
    "application/trig",
    "trig",
    "hext",
]

type TripleSerializeFormatOptions = TLiteral[
    "application/rdf+xml",
    "xml",
    "pretty-xml",
    "text/n3",
    "n3",
    "text/turtle",
    "turtle",
    "ttl",
    "longturtle",
    "application/n-triples",
    "ntriples",
    "nt",
    "nt11",
    "json-ld",
    "application/ld+json",
    "hext",
]

type QuadSerializeFormatOptions = TLiteral[
    "nquads",
    "application/n-quads",
    "trix",
    "application/trix",
    "trig",
    "application/trig",
]
