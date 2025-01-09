"""LODKit Triple utilities."""

from collections.abc import Callable, Iterator
from copy import deepcopy
from itertools import repeat
from typing import Any, Self, TypeAlias

from typeguard import check_type

from lodkit.lod_types import _Triple, _TripleObject, _TripleSubject
from loguru import logger
from rdflib import BNode, Graph, Literal, URIRef


_TPredicateObjectPair: TypeAlias = tuple[
    URIRef,
    _TripleObject
    | list
    | Iterator
    | Self  # type: ignore
    | str
    | tuple[_TripleObject | str, ...],
]


class ttl:
    """Triple constructor implementing a Turtle-like interface.
    The callable interface aims to provide a Python representation
    fo Turtle predicate and object list syntax.

    Args:
        uri (_TripleSubject): The subject of a triple
        *predicate_object_pairs (tuple[ URIRef, _TripleObject | list | Iterator | Self | str | tuple[_TripleObject, ...]]): Predicate-object pairs
        graph (Graph | None): An optional rdflib.Graph instance
        skip_if (Callable[[Any, Any, Any], bool]): Predicate for skipping triples. If True for a triple, the triple is skipped.
        Note that runtime checking for triple terms does not run if a skip_if predicate is provided.

    Returns:
        None

    Examples:

        triples: Iterator[lodkit._Triple] = ttl(
            URIRef('https://subject'),
            (RDF.type, URIRef('https://some_type')),
            (RDFS.label, Literal('label 1'), 'label 2'),
            (RDFS.seeAlso, [(RDFS.label, 'label 3')]),
            (RDFS.isDefinedBy, ttl(URIRef('https://subject_2'), (RDF.type, URI('https://another_type'))))
        )

        graph: Graph = triples.to_graph()
    """

    def __init__(
        self,
        uri: _TripleSubject,
        *predicate_object_pairs: _TPredicateObjectPair,
        graph: Graph | None = None,
        skip_if: Callable[[Any, Any, Any], bool] | None = None,
    ) -> None:
        self.uri = uri
        self.predicate_object_pairs = predicate_object_pairs
        self.graph = Graph() if graph is None else deepcopy(graph)
        self._iter = iter(self)
        self.skip_if = skip_if

        if self.skip_if is None:
            check_type(self.uri, _TripleSubject)
            check_type(self.predicate_object_pairs, tuple[_TPredicateObjectPair, ...])

    def __iter__(self) -> Iterator[_Triple]:
        """Generate an iterator of tuple-based triple representations."""
        _skip_if = (lambda s, p, o: False) if self.skip_if is None else self.skip_if

        for pred, obj in self.predicate_object_pairs:
            if _skip_if(self.uri, pred, obj):
                continue

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
                case obj if isinstance(obj, _TripleObject):
                    yield (self.uri, pred, obj)
                case str():
                    yield (self.uri, pred, Literal(obj))
                case _:
                    raise TypeError(
                        f"Unable to process triple object '{obj}'. "
                        "See the ttl docs and type annotation for applicable types "
                        "or skip respective triples using the skip_if predicate."
                    )

    def __next__(self) -> _Triple:
        """Return the next triple from the iterator."""
        return next(self._iter)

    def to_graph(self, graph: Graph | None = None) -> Graph:
        """Generate a graph instance from a ttl Iterator."""
        if graph is not None:
            graph_copy = deepcopy(graph)
            self.graph = graph_copy

        for triple in self:
            self.graph.add(triple)
        return self.graph


class plist(ttl):
    """Deprecated alias to ttl.

    This is for backwards api compatibility only.
    Since ttl also implements Turtle object lists now,
    refering to the class as "plist" is inaccurate/misleading.
    """

    def __init__(self, *args, **kwargs):
        logger.warning("Class 'plist' is a deprecated alias. Use 'ttl' instead.")
        super().__init__(*args, **kwargs)
