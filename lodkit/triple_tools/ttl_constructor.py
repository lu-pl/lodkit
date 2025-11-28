"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator

from lodkit.lod_types import _Triple, _TripleObject, _TripleSubject
from rdflib import BNode, Graph, Literal, RDF, URIRef


type _TPredicateObjectPairObject = (
    _TripleObject
    | str
    | list[_TPredicateObjectPair]
    | tuple[_TPredicateObjectPairObject, ...]
    | ttl
)

type _TPredicateObjectPair = tuple[URIRef, *tuple[_TPredicateObjectPairObject, ...]]


class ttl(Iterable[_Triple]):
    """Triple generation facility that implements a Turtle-like interface."""

    def __init__(
        self,
        subject: _TripleSubject,
        *predicate_object_pairs: _TPredicateObjectPair,
    ) -> None:
        self.subject = subject
        self.predicate_object_pairs = predicate_object_pairs

    def __iter__(self) -> Iterator[_Triple]:
        """Generate an iterator of 3-tuple triple representations."""

        for pred, *objs in self.predicate_object_pairs:
            for obj in objs:
                match obj:
                    case ttl():
                        yield (self.subject, pred, obj.subject)
                        yield from obj
                    case list():
                        _b = BNode()
                        yield (self.subject, pred, _b)
                        yield from ttl(_b, *obj)
                    case tuple():
                        first, *rest = obj
                        yield from ttl(
                            self.subject,
                            (
                                pred,
                                [
                                    (RDF.first, first),
                                    (RDF.rest, tuple(rest) or RDF.nil),
                                ],
                            ),
                        )
                    case obj if isinstance(obj, _TripleObject):
                        yield (self.subject, pred, obj)
                    case str():
                        yield (self.subject, pred, Literal(obj))
                    case _:
                        raise TypeError(
                            f"Unable to process triple object '{obj}'. "
                            "See the ttl docs and type annotation for applicable object types."
                        )

    def to_graph(self, graph: Graph | None = None) -> Graph:
        """Generate a graph instance from a ttl object."""
        _graph = Graph() if graph is None else graph

        for triple in self:
            _graph.add(triple)
        return _graph
