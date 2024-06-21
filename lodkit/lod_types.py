"""A collection of useful types for working with LOD."""

from collections.abc import Iterator
from typing import TypeAlias
from typing import Literal as TypingLiteral

from rdflib import BNode, Literal, URIRef
from rdflib.plugin import plugins
from rdflib.serializer import Serializer


_TripleSubject: TypeAlias = URIRef | BNode
_TripleObject: TypeAlias = Literal | URIRef | BNode
_RDFTerm: TypeAlias = _TripleObject
_Triple: TypeAlias = tuple[_TripleSubject, URIRef, _TripleObject]

_TripleLiteralObject: TypeAlias = tuple[URIRef, URIRef, Literal]
_TripleURIObject: TypeAlias = tuple[URIRef, URIRef, URIRef]
_TripleBNodeObject: TypeAlias = tuple[URIRef, URIRef, BNode]


def __graph_serialize_format_options() -> Iterator[str]:
    """Get rdflib.Graph.serialize format options (i.e. RDFLib plugin names)."""
    for plugin in plugins():
        if plugin.kind == Serializer:
            yield plugin.name


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
