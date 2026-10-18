"""LODKit Triple utilities."""

from collections.abc import Callable, Iterable, Iterator
from typing import Never

from rdflib import RDF, BNode, URIRef

from lodkit.triple_tools.literal import literal
from lodkit.triple_tools.utils import _ToGraphMixin
from lodkit.types import Triple, TripleObject, TripleSubject, TypedLiteral

type TripleSubjectFactory = Callable[[], TripleSubject]

type PredicateObjectPairObject = (
    TripleObject
    | str
    | TypedLiteral
    | list[PredicateObjectPair]
    | tuple[PredicateObjectPairObject, ...]
    | ttl
)

type PredicateObjectPair = tuple[
    URIRef, PredicateObjectPairObject, *tuple[PredicateObjectPairObject, ...]
]


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
    def subject(self) -> TripleSubject:
        match self._subject:
            case list() if not self._subject:
                return BNode()
            case URIRef() | BNode():
                return self._subject
            case Callable():
                return self._subject()
            case _:
                raise ValueError(
                    "Expected subject: TripleSubject | TripleSubjectFactory | list[Never]. "
                    f"Got '{self._subject}' instead."
                )

    @subject.setter
    def subject(
        self, subject: TripleSubject | TripleSubjectFactory | list[Never]
    ) -> None:
        self._subject = subject

    def __iter__(self) -> Iterator[Triple]:
        """Generate an iterator of 3-tuple triple representations."""
        subject = self.subject

        for pred, *objs in self.predicate_object_pairs:
            if not objs:
                raise ValueError(
                    f"Predicate-object pair for predicate '{pred}' has no object. "
                    "A property_value_pair must specify at least one object."
                )

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
                        if not obj:
                            yield (subject, pred, RDF.nil)
                            continue

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
                    case obj if isinstance(obj, (URIRef, BNode)):
                        yield (subject, pred, obj)
                    case _:
                        yield (subject, pred, literal(obj))
