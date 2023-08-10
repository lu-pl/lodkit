"""A collection of useful types for working with LOD."""

from typing import Literal as PyLiteral

from rdflib import Literal, URIRef

from rdflib.plugin import plugins
from rdflib.serializer import Serializer


_TripleObject = Literal | URIRef

_Triple = tuple[URIRef, URIRef, _TripleObject]

_TripleObjectLiteral = tuple[URIRef, URIRef, Literal]
_TripleObjectURI = tuple[URIRef, URIRef, URIRef]

rdflib_graph_format_options: str = [
    plugin.name for plugin
    in plugins()
    if plugin.kind == Serializer
    ]

_GraphFormatOptions = PyLiteral[*rdflib_graph_format_options]
