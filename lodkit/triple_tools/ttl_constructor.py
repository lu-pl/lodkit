"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator

from rdflib import BNode, Literal, RDF, URIRef

from lodkit.triple_tools.utils import _ToGraphMixin
from lodkit.types import Triple, TripleObject, TripleSubject


type TPredicateObjectPairObject = (
    TripleObject
    | str
    | list[TPredicateObjectPair]
    | tuple[TPredicateObjectPairObject, ...]
    | ttl
)

type TPredicateObjectPair = tuple[URIRef, *tuple[TPredicateObjectPairObject, ...]]


class ttl(Iterable[Triple], _ToGraphMixin):
    """Triple generation facility that implements a Turtle-like interface."""

    def __init__(
        self,
        subject: TripleSubject,
        *predicate_object_pairs: TPredicateObjectPair,
    ) -> None:
        self.subject = subject
        self.predicate_object_pairs = predicate_object_pairs

    def __iter__(self) -> Iterator[Triple]:
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
                    case obj if isinstance(obj, (URIRef, BNode, Literal)):
                        yield (self.subject, pred, obj)
                    case str():
                        yield (self.subject, pred, Literal(obj))
                    case _:
                        raise TypeError(
                            f"Unable to process triple object '{obj}'. "
                            "See the ttl docs and type annotation for applicable object types."
                        )
