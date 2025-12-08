"""A collection of useful types for working with LOD."""

from typing import Literal as TLiteral

from rdflib import BNode, Literal, URIRef


type TripleSubject = URIRef | BNode
type TriplePredicate = URIRef
type RDFTerm = Literal | URIRef | BNode
type TripleObject = RDFTerm
type Triple = tuple[TripleSubject, URIRef, TripleObject]

type LiteralObjectTriple = tuple[TripleSubject, URIRef, Literal]
type URIObjectTriple = tuple[TripleSubject, URIRef, URIRef]
type BNodeObjectTriple = tuple[TripleSubject, URIRef, BNode]

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
