"""LODKit Triple utilities."""

from collections.abc import Iterator
from itertools import repeat
from typing import Self, override

from lodkit.lod_types import _Triple, _TripleObject, _TripleSubject
from loguru import logger
from rdflib import BNode, Graph, Literal, URIRef


class ttl:
    """Triple/graph constructor implementing a ttl-like interface.

    The callable interface aims to provide a Python representation of
    Turtle predicate and object list syntax (';' and ',').
    See https://www.w3.org/TR/rdf12-turtle/#predicate-lists and
    https://www.w3.org/TR/rdf12-turtle/#object-lists.

    Example:

    triples = ttl(
        # 1. subject
        URIRef("https://subject.uri"),
        # 2. predicate lists
        # 2.1 predicate + object list
        (RDF.type, (lrm["F3_Manifestation"], crmdig["D1_Digital_Object"])),
        # 2.2 predicate + blank node object
        (crm["P1_is_identified_by"], [
            (RDF.type, crm["E41_Appellation"]),
            (crm["P190_has_symbolic_content"], Literal("Have more fun!"))
        ])
    )

    ttl.to_graph generates and returns an rdflib.Graph instance.
    """

    def __init__(
        self,
        uri: _TripleSubject,
        *predicate_object_pairs: tuple[URIRef, _TripleObject | list | Self | str],
        graph: Graph | None = None,
    ) -> None:
        """Initialize a ttl object."""
        self.uri = uri
        self.predicate_object_pairs = predicate_object_pairs
        self.graph = Graph() if graph is None else graph
        self._iter = iter(self)

    def __iter__(self) -> Iterator[_Triple]:
        """Generate an iterator of tuple-based triple representations."""
        for pred, obj in self.predicate_object_pairs:
            match obj:
                case ttl():
                    yield (self.uri, pred, obj.uri)
                    yield from obj
                case list() | Iterator():
                    _b = BNode()
                    yield (self.uri, pred, _b)
                    yield from ttl(_b, *obj)
                case tuple():
                    _object_list = zip(repeat(pred), obj)
                    yield from ttl(self.uri, *_object_list)
                case str():
                    yield (self.uri, pred, Literal(obj))
                case _:
                    yield (self.uri, pred, obj)

    def __next__(self) -> _Triple:
        """Return the next triple from the iterator."""
        return next(self._iter)

    def to_graph(self, graph: Graph | None = None) -> Graph:
        """Generate a graph instance from a ttl Iterator."""
        if graph is not None:
            self.graph = graph

        for triple in self:
            self.graph.add(triple)
        return self.graph


class plist(ttl):
    """Deprecated alias to ttl.

    This is for backwards api compatibility only.
    Since ttl also implements Turtle object lists now,
    refering to the class as "plist" is inaccurate/misleading.
    """

    @override
    def __init__(self, *args, **kwargs):
        logger.warning("Class 'plist' is a deprecated alias. Use 'ttl' instead.")
        super().__init__(*args, **kwargs)
