"""Triple tuples expected to fail lodkit.lod_types._Triple checks."""

from typing import Annotated, Any

from rdflib import BNode, Literal, URIRef


s = URIRef("https://test.org/test_subject")
p = URIRef("https://test.org/test_predicate")
o = URIRef("https://test.org/test_object")
l = Literal("test_literal")  # noqa: E741
b = BNode()


fail_triples: Annotated[
    list[tuple[Any, Any, Any]],
    """Fail cases:
    1. Literal in s, p
    2. BNode in p
    3. str in o
    """,
] = [
    (l, p, o),
    (s, l, o),
    (s, b, o),
    (s, p, "test string"),
]
