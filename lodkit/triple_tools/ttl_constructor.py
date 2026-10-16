"""LODKit Triple utilities."""

from collections.abc import Callable, Iterable, Iterator
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
type TripleSubjectFactory = Callable[[], TripleSubject]


class ttl(Iterable[Triple], _ToGraphMixin):
    """Triple generation facility that implements a Turtle-like interface."""

    def __init__(
        self,
        subject: TripleSubject | TripleSubjectFactory | list[Never],
        *predicate_object_pairs: PredicateObjectPair,
    ) -> None:
        self._subject = subject
        self.predicate_object_pairs = predicate_object_pairs

    @property
    def subject(self):
        match self._subject:
            case list() if not self._subject:
                return BNode()
            case URIRef() | BNode():
                return self._subject
            case Callable():
                return self._subject()
            case _:
                msg = (
                    "Expected subject: TripleSubject | TripleSubjectFactory | list[Never]. "
                    f"Got '{self._subject}' instead."
                )
                raise TypeError(msg)

    @subject.setter
    def subject(
        self, subject: TripleSubject | TripleSubjectFactory | list[Never]
    ) -> None:
        self._subject = subject

    def __iter__(self) -> Iterator[Triple]:
        """Generate an iterator of 3-tuple triple representations."""
        subject = self.subject

        for pred, *objs in self.predicate_object_pairs:
            for obj in objs:
                match obj:
                    case ttl():
                        object_subject = obj.subject
                        yield (subject, pred, object_subject)
                        yield from ttl(object_subject, *obj.predicate_object_pairs)
                    case list():
                        _b = BNode()
                        yield (subject, pred, _b)
                        yield from ttl(_b, *obj)
                    case tuple():
                        first, *rest = obj
                        yield from ttl(
                            subject,
                            (
                                pred,
                                [
                                    (RDF.first, first),
                                    (RDF.rest, tuple(rest) or RDF.nil),
                                ],
                            ),
                        )
                    case obj if isinstance(obj, (URIRef, BNode, Literal)):
                        yield (subject, pred, obj)
                    case str():
                        yield (subject, pred, Literal(obj))
                    case _:
                        raise TypeError(
                            f"Unable to process triple object '{obj}'. "
                            "See the ttl docs and type annotation for applicable object types."
                        )
