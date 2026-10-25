from typing import get_args

from rdflib import Literal

from lodkit.types import TypedLiteral

_typed_literal_types: tuple[type, ...] = get_args(TypedLiteral.__value__)


def literal(obj: object) -> Literal:
    """Convert obj to a "sane" rdflib.Literal.

    Literal and str objects are forwarded as untyped literals.
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
