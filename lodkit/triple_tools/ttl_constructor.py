"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator
from typing import Never

from rdflib import RDF, BNode, Literal, URIRef

from lodkit.triple_tools.utils import _ToGraphMixin
from lodkit.types import Triple, TripleObject, TripleSubject

type PredicateObjectPairObject = (
    TripleObject
    | str
    | list[PredicateObjectPair]
    | tuple[PredicateObjectPairObject, ...]
    | ttl
)

type PredicateObjectPair = tuple[URIRef, *tuple[PredicateObjectPairObject, ...]]


class ttl(Iterable[Triple], _ToGraphMixin):
    """Triple generation facility that implements a Turtle-like interface."""

    def __init__(
        self,
        subject: TripleSubject | list[Never],
        *predicate_object_pairs: PredicateObjectPair,
    ) -> None:
        self._subject = subject
        self.predicate_object_pairs = predicate_object_pairs

    @property
    def subject(self):
        match self._subject:
            case list() if not self._subject:
                return BNode()
            case _:
                return self._subject

    @subject.setter
    def subject(self, subject: TripleSubject | list[Never]) -> None:
        self._subject = subject

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
