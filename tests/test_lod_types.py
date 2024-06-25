"""Tests for lodkit.lod_types."""

import pytest
from typeguard import TypeCheckError, check_type

from lodkit import (
    _Triple,
    _TripleBNodeObject,
    _TripleLiteralObject,
    _TripleObject,
    _TripleSubject,
    _TripleURIObject,
)
from tests.data.fail_triples import fail_triples
from tests.utils.paths import ontologies_path
from tests.utils.utils import parametrize_graphs_from_glob


@parametrize_graphs_from_glob(ontologies_path, param="graph")
def test_triple_type(graph):
    """Runtime check if every triple in graphs is of type lodkit._Triple."""
    for triple in graph.triples((None, None, None)):
        check_type(triple, _Triple)
        assert True


@parametrize_graphs_from_glob(ontologies_path, param="graph")
def test_triple_subject_object_type(graph):
    """Runtime check for lodkit._TripleSubject and lodkit._TripleObject."""
    for s, _, o in graph.triples((None, None, None)):
        check_type(s, _TripleSubject)
        check_type(o, _TripleObject)


@parametrize_graphs_from_glob(ontologies_path, param="graph")
def test_triple_object_types(graph):
    """Runtime check for _TripleURI|BNode|LiteralObject."""
    for triple in graph.triples((None, None, None)):
        check_type(triple, _TripleURIObject | _TripleBNodeObject | _TripleLiteralObject)


@pytest.mark.parametrize("fail_triple", fail_triples)
def test_triple_type_fails(fail_triple):
    """Invoke lodkit.lod_types runtime checks on triples excpected to fail."""
    with pytest.raises(TypeCheckError):
        check_type(fail_triple, _Triple)
