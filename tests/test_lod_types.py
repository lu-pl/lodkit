"""Tests for lodkit.lod_types."""

from lodkit import (
    _BNodeObjectTriple,
    _GraphParseFormatOptions,
    _GraphSerializeFormatOptions,
    _LiteralObjectTriple,
    _QuadParseFormatOptions,
    _QuadSerializeFormatOptions,
    _Triple,
    _TripleObject,
    _TripleParseFormatOptions,
    _TripleSerializeFormatOptions,
    _TripleSubject,
    _URIObjectTriple,
)
import pytest
from tests.data.fail_triples import fail_triples
from tests.utils.paths import ontologies_path
from tests.utils.utils import parametrize_graphs_from_glob
from typeguard import TypeCheckError, check_type


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
        check_type(triple, _URIObjectTriple | _BNodeObjectTriple | _LiteralObjectTriple)


@pytest.mark.parametrize("fail_triple", fail_triples)
def test_triple_type_fails(fail_triple):
    """Invoke lodkit.lod_types runtime checks on triples excpected to fail."""
    with pytest.raises(TypeCheckError):
        check_type(fail_triple, _Triple)


def test_sum_serialize_options_type():
    """Check if the sum of triple and quad serialize option Literal values is equal to the sum of all serialize options."""
    len_all_options: int = len(_GraphSerializeFormatOptions.__args__)
    len_triple_options: int = len(_TripleSerializeFormatOptions.__args__)
    len_quad_options: int = len(_QuadSerializeFormatOptions.__args__)

    assert len_triple_options + len_quad_options == len_all_options


def test_sum_parse_options_type():
    """Check if the sum of triple and quad parse option Literal values is equal to the sum of all parse options."""
    len_all_options: int = len(_GraphParseFormatOptions.__args__)
    len_triple_options: int = len(_TripleParseFormatOptions.__args__)
    len_quad_options: int = len(_QuadParseFormatOptions.__args__)

    assert len_triple_options + len_quad_options == len_all_options
