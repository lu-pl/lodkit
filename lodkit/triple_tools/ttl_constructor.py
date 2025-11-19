"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator
import functools
from itertools import repeat
import itertools
from typing import Self

from lodkit.lod_types import _Triple, _TripleObject, _TripleSubject
from rdflib import BNode, Graph, Literal, URIRef


type _TPredicateObjectPairObject = (
    _TripleObject
    | str
    | list[_TPredicateObjectPair]
    | Iterator[_TPredicateObjectPair]
    | tuple[_TPredicateObjectPairObject, ...]
    | ttl
)

type _TPredicateObjectPair = tuple[URIRef, _TPredicateObjectPairObject]


class _ToGraphMixin:
    def to_graph(self: Iterable[_Triple], graph: Graph | None = None) -> Graph:
        """Generate a graph instance from a ttl Iterator."""
        _graph = Graph() if graph is None else graph

        for triple in self:
            _graph.add(triple)
        return _graph


class TripleChain(Iterator[_Triple], _ToGraphMixin):
    def __init__(self, *triples: Iterable[_Triple]) -> None:
        self._triples = itertools.chain.from_iterable(triples)

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> _Triple:
        return next(self._triples)

    def __or__(self, other: Iterable[_Triple]) -> Self:
        return self.__class__(self, other)


class ttl(Iterable[_Triple], _ToGraphMixin):
    def __init__(
        self,
        uri: _TripleSubject,
        *predicate_object_pairs: _TPredicateObjectPair,
    ) -> None:
        self.uri = uri
        self.predicate_object_pairs = predicate_object_pairs

    def __iter__(self) -> Iterator[_Triple]:
        """Generate an iterator of 3-tuple triple representations."""

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
                case obj if isinstance(obj, _TripleObject):
                    yield (self.uri, pred, obj)
                case str():
                    yield (self.uri, pred, Literal(obj))
                case _:
                    raise TypeError(
                        f"Unable to process triple object '{obj}'. "
                        "See the ttl docs and type annotation for applicable object types."
                    )

    def __or__(self, other: Iterable[_Triple]) -> TripleChain:
        return TripleChain(self, other)
