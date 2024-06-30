"""Happy path tests for ttl triple constructor."""

from collections import Counter
from collections.abc import Iterator
from typing import Annotated

from hypothesis import given, strategies as st
from lodkit import tst_xml, ttl
from lodkit.testing_tools.graph_format_options import triple_serialize_format_options
import pytest
from rdflib import BNode, Graph, URIRef
from rdflib.compare import graph_diff, isomorphic
from tests.data.graphs.ontologies import owl
from tests.utils.strategies import (
    untyped_predicate_object_pairs,
    predicate_iterator_pairs,
    predicate_list,
    predicate_object_pairs,
    predicate_pair_pairs,
    predicate_ttl_pairs,
)


@given(uri=tst_xml.triple_subjects, pair=predicate_object_pairs)
def test_ttl_single_triple(uri, pair):
    """Test for single triple ttl instantiation."""
    triples = ttl(uri, pair)
    graph = triples.to_graph()

    assert len(list(triples)) == len(graph) == 1


@pytest.mark.slow
@given(pairs=st.lists(predicate_object_pairs, min_size=50, max_size=50))
def test_ttl_multi_triples(pairs):
    """Test for multiple triple ttl instantiation."""
    triples = ttl(BNode(), *pairs)
    graph = triples.to_graph()

    assert len(list(triples)) == len(graph)


@given(uri=tst_xml.triple_subjects, pair=predicate_object_pairs)
def test_ttl_single_triple_serialize(uri, pair):
    """Test for single triple ttl graph casting and serialization."""
    graph = ttl(uri, pair).to_graph()

    for _format in triple_serialize_format_options:
        assert graph.serialize(format=_format)


@pytest.mark.slow
@given(pairs=st.lists(predicate_object_pairs, min_size=50, max_size=50))
def test_ttl_multi_triples_serialize(pairs):
    """Test for multiple triple ttl graph casting and serialization."""
    graph = ttl(BNode(), *pairs).to_graph()

    for _format in triple_serialize_format_options:
        assert graph.serialize(format=_format)


@given(pairs=predicate_pair_pairs)
def test_ttl_bnode_object(pairs):
    """Test for ttl bnode object instantiation."""
    triples = ttl(BNode(), pairs)
    assert len(list(triples)) == (len(pairs[1]) + 1)


@given(pairs=predicate_pair_pairs)
def test_ttl_bnode_object_serialize(pairs):
    """Test for ttl bnode object graph casting and serialization."""
    graph = ttl(BNode(), pairs).to_graph()

    for _format in triple_serialize_format_options:
        assert graph.serialize(format=_format)


@given(predicate_list)
def test_ttl_predicate_list(predicate_list):
    """Test for ttl predicate list instantiation."""
    triples = ttl(
        URIRef(f"https://lodkit.testing_tools/subject"),
        (URIRef(f"https://lodkit.testing_tools/predicate"), predicate_list),
    )
    assert len(list(triples)) == len(predicate_list) > 0


@given(predicate_list)
def test_ttl_predicate_list_serialize(predicate_list):
    """Test for ttl predicate list graph casting + serialization."""
    triples = ttl(
        URIRef(f"https://lodkit.testing_tools/subject"),
        (URIRef(f"https://lodkit.testing_tools/predicate"), predicate_list),
    )
    graph = triples.to_graph()

    for _format in triple_serialize_format_options:
        assert graph.serialize(format=_format)


@given(pairs=untyped_predicate_object_pairs)
def test_ttl_serialize_parse_isomorphic(pairs):
    """Test for ttl.to_graph serialization and parsing.

    Note: Actually this mainly tests RDFLib;
    'hext' and 'xml' serialization formats do not pass this test,
    for 'xml' this is likely a problem with SaxParser ('\x08' and '\x1f' are rejected as literals),
    for 'hext' this might actually be a problem in the RDFLib parse plugin. -> Report this!

    Note: Also xsd-typed literals do not pass this tests.
    Apparently types get dropped on parsing...
    """
    graph = ttl(URIRef("https://lodkit.testing_tools/subject/"), pairs).to_graph()

    for _format in ["ttl", "n3", "ntriples"]:
        serialized: str = graph.serialize(format=_format)
        graph_parsed: Graph = Graph().parse(data=serialized, format=_format)

        assert isomorphic(graph, graph_parsed)


@given(uri=tst_xml.triple_subjects, pair=predicate_object_pairs)
def test_ttl_single_triple_graph_init(uri, pair):
    """Test for single triple ttl initialized with graph."""
    triples = ttl(uri, pair, graph=owl)
    graph = triples.to_graph()

    assert len(graph) == (len(list(triples)) + len(owl))


@pytest.mark.slow
@given(pairs=st.lists(predicate_object_pairs, min_size=50, max_size=50))
def test_ttl_multi_triples_graph_init(pairs):
    """Test for multiple triple ttl initialized with graph."""
    triples = ttl(BNode(), *pairs, graph=owl)
    graph = triples.to_graph()

    assert len(graph) == (len(list(triples)) + len(owl))


@given(uri=tst_xml.triple_subjects, pair=predicate_object_pairs)
def test_ttl_single_triple_to_graph(uri, pair):
    """Test for single triple ttl.to_graph."""
    triples = ttl(uri, pair)
    graph = triples.to_graph(owl)

    assert len(graph) == (len(list(triples)) + len(owl))


@pytest.mark.slow
@given(pairs=st.lists(predicate_object_pairs, min_size=50, max_size=50))
def test_ttl_multi_triples_to_graph(pairs):
    """Test for multiple triple ttl.to_graph."""
    triples = ttl(BNode(), *pairs)
    graph = triples.to_graph(owl)

    assert len(graph) == (len(list(triples)) + len(owl))


@given(predicate_ttl_pair=predicate_ttl_pairs)
def test_ttl_ttl_object_no_bnodes(predicate_ttl_pair):
    """Pass ttl instances as objects to ttl and check that no bnodes are created.

    Note: ttl instances are Iterators but ttl is checked first in ttl's match clause.
    See also test_ttl_iterator_bnodes().
    """
    triples = ttl(URIRef("subject"), predicate_ttl_pair)
    assert not any(isinstance(subj, BNode) for subj, *_ in triples)


@given(predicate_iterator_pair=predicate_iterator_pairs)
def test_ttl_iterator_bnodes(predicate_iterator_pair):
    """Pass iterators as objects to ttl and check that bnodes /are/ created.

    More precise: Check that the number of triples in the graph -1
    is equal to the number of bnodes in the graph.
    """
    triples = ttl(URIRef("subject"), predicate_iterator_pair)
    graph = triples.to_graph()

    assert (len(graph) - 1) == len(
        [s for s in graph.subjects() if isinstance(s, BNode)]
    )
