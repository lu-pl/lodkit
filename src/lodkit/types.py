"""A collection of useful types for working with LOD."""

import datetime
import decimal
from fractions import Fraction
from pathlib import PurePath
from typing import IO, TextIO
from typing import Literal as TLiteral
from xml.dom.minidom import Document

from rdflib import BNode, Literal, URIRef
from rdflib.parser import InputSource
from rdflib.xsd_datetime import Duration

__all__ = (
    "BNodeObjectTriple",
    "GraphParseFormatOptions",
    "GraphSerializeFormatOptions",
    "LiteralObjectTriple",
    "QuadParseFormatOptions",
    "QuadSerializeFormatOptions",
    "RDFTerm",
    "Triple",
    "TripleObject",
    "TripleParseFormatOptions",
    "TriplePredicate",
    "TripleSerializeFormatOptions",
    "TripleSubject",
    "TypedLiteral",
    "URIObjectTriple",
)

type TripleSubject = URIRef | BNode
type TriplePredicate = URIRef
type RDFTerm = Literal | URIRef | BNode
type TripleObject = RDFTerm
type Triple = tuple[TripleSubject, URIRef, TripleObject]

type LiteralObjectTriple = tuple[TripleSubject, URIRef, Literal]
type URIObjectTriple = tuple[TripleSubject, URIRef, URIRef]
type BNodeObjectTriple = tuple[TripleSubject, URIRef, BNode]

type TypedLiteral = (
    bool
    | int
    | float
    | decimal.Decimal
    | datetime.date
    | datetime.datetime
    | datetime.time
    | datetime.timedelta
    | Duration
    | Document
    | Fraction
)
"""Union of Python types for which rdflib.Literal(obj) reliably computes a typed RDF literal.

lodkit.TypedLiteral describes an encode-direction contract:
obj is a member of this type exactly if Literal(obj) produces a typed RDF literal.

For the rdflib.Literal.toPython decode-direction union type see lodkit.LiteralToPython.
Note that lodkit.TypedLiteral and lodkit.LiteralToPython overlap heavily but
neither is a strict subset of the other (see the respective docs).

The following Python types are not members of TypedLiteral:

    - str: Literal(str_obj) always yields an untyped literal in RDFLib.
    - Literal: rdflib.Literal objects as inputs to rdflib.Literal are simply forwarded;
      although this preserves the RDF type of the rdflib.Literal object argument,
      untyped rdflib.Literal objects remain untyped.
    - None: Literal(None) silently produces an untyped Literal('None') -
      this is arguably a footgun.

rdflib.compat.long_type is int on Python 3, so it is not listed separately.
"""

type LiteralToPython = (
    Literal
    | None
    | str
    | bytes
    | bool
    | int
    | float
    | decimal.Decimal
    | datetime.date
    | datetime.datetime
    | datetime.time
    | datetime.timedelta
    | Duration
    | Document
)
"""Return type for rdflib.Literal.toPython.

This union type represents all possible return value types of Literal.toPython.

Note that lodkit.LiteralToPython overlaps heavily with lodkit.TypedLiteral;
both describe what rdflib.Literal considers a typed value from opposite directions,
but neither is a strict subset of the other:

    - fractions.Fraction is in lodkit.TypedLiteral but not in lodkit.LiteralToPython:
      it encodes to a real datatype but is not round-tripable.
    - Literal, None, str and bytes are members of lodkit.LiteralToPython but not in lodkit.TypedLiteral:
      those types are decode-side outcomes (a conversion giving up, or a plain-literal
      lexical form) with no typed-encode counterpart.

Return type provenance:

    - Literal: rdflib.Literal.toPython
    - None: rdflib.term._castLexicalToPython
    - str: rdflib.term._castLexicalToPython's direct str(lexical) fallback,
      taken for plain literals, lang-tagged literals, and any datatype whose
      XSDToPython entry is None (xsd:string, xsd:normalizedString, xsd:token,
      xsd:language, xsd:anyURI)

    - datetime.datetime: rdflib.xsd_datetime.parse_datetime
    - datetime.time: rdflib.xsd_datetime.parse_time
    - datetime.timedelta, Duration: parse_xsd_duration
    - bytes: rdflib.term._unhexlify, base64.b64decode
    - bool: rdflib.term._parseBoolean
    - int, float, decimal.Decimal: rdflib.term.XSDToPython
      (rdflib.compat.long_type maps here too, but it is int on Python 3)
    - Document: rdflib.term._parseXML
"""

type GraphParseSource = IO[bytes] | TextIO | InputSource | str | bytes | PurePath
"""Source parameter type for rdflib.Graph.parse.

This is the exact union type as defined in RDFLib.
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
