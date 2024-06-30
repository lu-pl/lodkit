"""Tests for graph_format_options."""

from hypothesis import given
from lodkit.testing_tools.graph_format_options import (
    get_parse_format_from_serialize_format,
    graph_parse_format_options,
    graph_serialize_format_options,
    quad_parse_format_options,
    quad_serialize_format_options,
    triple_parse_format_options,
    triple_serialize_format_options,
)
from rdflib import Dataset, Graph, URIRef
from tests.utils.strategies import ttl_instances


def test_sum_serialize_options():
    """Check if the sum of triple and quad serialize options is equal to the sum of all serialize options."""
    len_all_options: int = len(graph_serialize_format_options)
    len_triple_options: int = len(triple_serialize_format_options)
    len_quad_options: int = len(quad_serialize_format_options)

    assert len_triple_options + len_quad_options == len_all_options


def test_sum_parse_options():
    """Check if the sum of triple and quad parse options is equal to the sum of all parse options."""
    len_all_options: int = len(graph_parse_format_options)
    len_triple_options: int = len(triple_parse_format_options)
    len_quad_options: int = len(quad_parse_format_options)

    assert len_triple_options + len_quad_options == len_all_options


@given(ttl_instances)
def test_serialize_triple_options(ttl_instance):
    """Serialize a test graph with all available triple format options."""
    graph: Graph = ttl_instance.to_graph()

    for _format in triple_serialize_format_options:
        assert graph.serialize(format=_format)


@given(ttl_instances)
def test_parse_triple_options(ttl_instance):
    """Serialize and then parse a test graph with all available triple format options."""
    graph: Graph = ttl_instance.to_graph()

    for _format in triple_serialize_format_options:
        serialized: str = graph.serialize(format=_format)
        parse_format = get_parse_format_from_serialize_format(_format)

        parsed_graph = Graph().parse(data=serialized, format=parse_format)
        assert parsed_graph


@given(ttl_instances)
def test_serialize_quad_options(ttl_instance):
    """Serialize a test dataset with all available quad format options."""
    triples = ttl_instance
    dataset = Dataset()
    dataset.graph(URIRef("https://lodkit.testing/named_graph/"))

    for triple in triples:
        dataset.add(triple)

    for _format in quad_serialize_format_options:
        assert dataset.serialize(format=_format)


@given(ttl_instances)
def test_parse_quad_options(ttl_instance):
    """Serialize a test dataset with all available quad format options."""
    triples = ttl_instance
    dataset = Dataset()
    dataset.graph(URIRef("https://lodkit.testing/named_graph/"))

    for triple in triples:
        dataset.add(triple)

    for _format in quad_serialize_format_options:
        serialized: str = dataset.serialize(format=_format)

        parsed_dataset = Dataset().parse(data=serialized, format=_format)
        assert parsed_dataset
