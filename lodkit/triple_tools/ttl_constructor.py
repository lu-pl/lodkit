"""LODKit Triple utilities."""

from collections.abc import Iterable, Iterator
from typing import Never, get_args

from rdflib import RDF, BNode, Literal, URIRef

from lodkit.triple_tools.utils import _ToGraphMixin
from lodkit.types import Triple, TripleObject, TripleSubject, TypedLiteral

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


_typed_literal_types: tuple[type, ...] = get_args(TypedLiteral.__value__)


def _to_literal(obj: object) -> Literal:
    """Convert obj to a sane rdflib.Literal.

    Literal and str objects are forwared as untyped literals.
    Any other Python object is runtime-checked against lodkit.TypedLiteral
    and raises ValueError for objects that do not correspond to typed RDF literals.
    """
    match obj:
        case Literal():
            return obj
        case str():
            return Literal(obj)
        case obj if isinstance(obj, _typed_literal_types):
            return Literal(obj)
        case _:
            raise ValueError(
                f"Unable to convert object '{obj!r}' of type '{type(obj).__name__}' "
                "to a typed Literal. Pass an explicit rdflib.Literal if an "
                "untyped literal is intended."
            )


class ttl(Iterable[Triple], _ToGraphMixin):
    """Triple generation facility that implements a Turtle-like interface."""

    def __init__(
        self,
        subject: TripleSubject | list[Never],
        *predicate_object_pairs: PredicateObjectPair,
    ) -> None:
        self.subject = BNode() if subject == [] else subject
        self.predicate_object_pairs = predicate_object_pairs

    def __iter__(self) -> Iterator[Triple]:
        """Generate an iterator of 3-tuple triple representations."""

        for pred, *objs in self.predicate_object_pairs:
            if not objs:
                raise ValueError(
                    f"Predicate-object pair for predicate '{pred}' has no object. "
                    "A property_value_pair must specify at least one object."
                )

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
                        if not obj:
                            yield (self.subject, pred, RDF.nil)
                            continue

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
                    case obj if isinstance(obj, (URIRef, BNode)):
                        yield (self.subject, pred, obj)
                    case _:
                        yield (self.subject, pred, _to_literal(obj))
