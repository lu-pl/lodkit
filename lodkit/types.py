"""A collection of useful types for working with LOD."""

from rdflib import Literal, URIRef


_TripleObject = Literal | URIRef

_Triple = tuple[URIRef, URIRef, _TripleObject]

_TripleObjectLiteral = tuple[URIRef, URIRef, Literal]
_TripleObjectURI = tuple[URIRef, URIRef, URIRef]
