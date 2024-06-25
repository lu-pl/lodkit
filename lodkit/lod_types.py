"""A collection of useful types for working with LOD."""

from collections.abc import Iterator
from typing import TypeAlias
from typing import Literal as TypingLiteral

from rdflib import BNode, Literal, URIRef


_TripleSubject: TypeAlias = URIRef | BNode
_TriplePredicate: TypeAlias = URIRef
_TripleObject: TypeAlias = Literal | URIRef | BNode
_RDFTerm: TypeAlias = _TripleObject
_Triple: TypeAlias = tuple[_TripleSubject, URIRef, _TripleObject]

_TripleLiteralObject: TypeAlias = tuple[_TripleSubject, URIRef, Literal]
_TripleURIObject: TypeAlias = tuple[_TripleSubject, URIRef, URIRef]
_TripleBNodeObject: TypeAlias = tuple[_TripleSubject, URIRef, BNode]


_GraphFormatOptions: TypeAlias = TypingLiteral[
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
