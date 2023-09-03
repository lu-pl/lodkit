"""LODKit utilities."""


import collections
import hashlib

from typing import Callable

from rdflib import Graph, URIRef
from lodkit.types import _TripleObject


class plist(collections.UserList):
    """Shorthand for referencing a triple subject by multiple predicates.

    Basically a Python representation of what is expressed in ttl with ';'.
    See https://www.w3.org/TR/turtle/#predicate-lists.

    E.g. the following creates a list of 3 triples relating to a single subject:

    plist(
        URIRef("http://example.org/#green-goblin"),
        (REL.enemyOF, URIRef("http://example.org/#spiderman")),
        (RDF.type, FOAF.Person),
        (FOAF.name, "Green Goblin")
    )
    """

    def __init__(self,
                 subject: URIRef,
                 *predicate_object_pairs: tuple[URIRef, _TripleObject],
                 graph: Graph | None = None):
        """Initialize a predicate list instance."""
        super().__init__()
        self.graph = Graph() if graph is None else graph

        for pair in predicate_object_pairs:
            self.data.append((subject, *pair))

    def to_graph(self):
        """Add triples to a graph instance and return."""
        for triple in self.data:
            self.graph.add(triple)

        return self.graph

    def __repr__(self):  # noqa D105
        return f"plist({self.data})"



def genhash(input: str,
            length: int | None = 10,
            hash_function: Callable = hashlib.sha256) -> str:
    """Generate a truncated URL-safe string hash.

    Pass length=None for an untruncated hash.
    """
    _hash = hash_function(input.encode('utf-8')).hexdigest()
    return _hash[:length]
