"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator
from itertools import repeat

from lodkit.lod_types import _Triple, _TripleObject, _TripleSubject
from rdflib import BNode, Graph, Literal, URIRef


type _TPredicateObjectPair = tuple[
    URIRef,
    ttl | _TripleObject | list | Iterator | str | tuple[_TripleObject | str, ...],
]


class ttl(Iterable[_Triple]):
    """Triple generation facility that implements a Turtle-like interface.

    The generator takes a triple subject and an aribitrary number of predicate/object pairs
    and produces an Iterator of RDFLib object 3-tuples.

    Triple objects passed to the constructor can be
    - URIRefs, BNodes, Literals
    - Python lists of predicate/object tuples (resolved as blank nodes),
    - tuples (resolved as Turtle object lists)
    - ttl constructors (resolved recursively)

    Args:
        uri (_TripleSubject): The subject of a triple
        *predicate_object_pairs (tuple[ URIRef, _TripleObject | list | Iterator | Self | str | tuple[_TripleObject, ...]]): Predicate-object pairs

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

    def to_graph(self, graph: Graph | None = None) -> Graph:
        """Generate a graph instance from a ttl Iterator."""
        _graph = Graph() if graph is None else graph

        for triple in self:
            _graph.add(triple)
        return _graph
