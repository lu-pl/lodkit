"""A collection of useful types for working with LOD."""

from typing import Literal as TLiteral

from rdflib import BNode, Literal, URIRef


type _TripleSubject = URIRef | BNode
type _TriplePredicate = URIRef
type _RDFTerm = Literal | URIRef | BNode
type _TripleObject = _RDFTerm
type _Triple = tuple[_TripleSubject, URIRef, _TripleObject]

type _LiteralObjectTriple = tuple[_TripleSubject, URIRef, Literal]
type _URIObjectTriple = tuple[_TripleSubject, URIRef, URIRef]
type _BNodeObjectTriple = tuple[_TripleSubject, URIRef, BNode]

type _GraphParseFormatOptions = TLiteral[
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

type _TripleParseFormatOptions = TLiteral[
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

type _QuadParseFormatOptions = TLiteral[
    "nquads",
    "application/n-quads",
    "trix",
    "application/trix",
    "trig",
    "application/trig",
]

type _GraphSerializeFormatOptions = TLiteral[
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

type _TripleSerializeFormatOptions = TLiteral[
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

type _QuadSerializeFormatOptions = TLiteral[
    "nquads",
    "application/n-quads",
    "trix",
    "application/trix",
    "trig",
    "application/trig",
]
