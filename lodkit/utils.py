"""LODKit utilities."""

import hashlib

from typing import Callable, Generator, Optional

from rdflib import BNode, Graph, URIRef
from lodkit.types import _TripleObject


class plist:
    """Shorthand for referencing a triple subject by multiple predicates.

    Basically a Python representation of what is expressed in ttl with ';'.
    See https://www.w3.org/TR/turtle/#predicate-lists.

    E.g. the following creates a list of 3 triples relating to a single subject:

    plist(
        URIRef("http://example.org/#green-goblin"),
        (REL.enemyOF, URIRef("http://example.org/#spiderman")),
        (RDF.type, FOAF.Person),
        (FOAF.name, Literal("Green Goblin"))
    )

    Also BNodes are supported with the following notation:

    plist(
        URIRef("http://example.org/#green-goblin"),
        (RDF.type, FOAF.Person),
        (FOAF.name, Literal("Green Goblin")),
        (REL.enemyOF, [
            (RDF.type, FOAF.Person),
            (FOAF.name, Literal("Spiderman"))
        ]),
    )

    plist.to_graph generates and returns an rdflib.Graph instance.
    """

    def __init__(self,
                 uri: URIRef,
                 *predicate_object_pairs: tuple[URIRef, _TripleObject | list],
                 graph: Optional[Graph] = None):
        """Initialize a plist object."""
        self.uri = uri
        self.predicate_object_pairs = predicate_object_pairs
        self.graph = Graph() if graph is None else graph

    def __iter__(self) -> Generator:
        """Generate an iterator of tuple-based triple representations."""
        for pred, obj in self.predicate_object_pairs:
            if isinstance(obj, list):
                _b = BNode()
                yield from plist(_b, *obj)
                yield (self.uri, pred, _b)
                continue
            yield (self.uri, pred, obj)

    def to_graph(self) -> Graph:
        """Generate a graph instance."""
        for triple in self:
            self.graph.add(triple)
        return self.graph


def genhash(input: str,
            length: int | None = 10,
            hash_function: Callable = hashlib.sha256) -> str:
    """Generate a truncated URL-safe string hash.

    Pass length=None for an untruncated hash.
    """
    _hash = hash_function(input.encode('utf-8')).hexdigest()
    return _hash[:length]
