"""Happy path tests for the skip_if feature of lodkit.ttl."""

from collections.abc import Callable, Iterable
from typing import Any, NamedTuple

import pytest

from lodkit import ttl
from rdflib import Literal, URIRef


class Parameter(NamedTuple):
    subject: Any
    predicate_object_pairs: Iterable[tuple[Any, Any]]
    skip_if: Callable[[Any, Any, Any], bool]
    expected_triple_count: int


parameters = [
    Parameter(
        subject=URIRef("subject"),
        predicate_object_pairs=[
            (URIRef("predicate"), "literal"),
            (URIRef("predicate"), "forbidden predicate"),
        ],
        skip_if=lambda s, p, o: o == "forbidden predicate",
        expected_triple_count=1,
    ),
    Parameter(
        subject=URIRef("subject"),
        predicate_object_pairs=[
            (URIRef("predicate"), "literal"),
            (URIRef("predicate"), None),
        ],
        skip_if=lambda s, p, o: o is None,
        expected_triple_count=1,
    ),
    Parameter(
        subject=URIRef("subject"),
        predicate_object_pairs=[
            (URIRef("predicate"), "literal"),
            (URIRef("forbidden_predicate"), "literal"),
        ],
        skip_if=lambda s, p, o: p == URIRef("forbidden_predicate"),
        expected_triple_count=1,
    ),
    Parameter(
        subject=URIRef("forbidden subject"),
        predicate_object_pairs=[
            (URIRef("predicate"), "literal"),
        ],
        skip_if=lambda s, p, o: s == URIRef("forbidden subject"),
        expected_triple_count=0,
    ),
]


@pytest.mark.parametrize("param", parameters)
def test_ttl_skip_if(param):
    graph = ttl(
        param.subject,
        *param.predicate_object_pairs,
        skip_if=param.skip_if,
    ).to_graph()

    assert len(graph) == param.expected_triple_count
