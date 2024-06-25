"""Tests for tests.utils.utils."""

from pathlib import Path

from rdflib import Graph
from tests.utils.paths import ontologies_path
from tests.utils.utils import (
    parametrize_graphs_from_glob,
    parametrize_paths_from_glob,
    parametrize_serializations_from_graph,
)

test_graph = Graph().parse("./data/graphs/ontologies/owl.ttl")


@parametrize_serializations_from_graph(test_graph, "whatever")
def test_ok(whatever):
    graph_obj = Graph().parse(whatever.name)

    assert isinstance(graph_obj, Graph)
    assert len(graph_obj) > 0


@parametrize_paths_from_glob(ontologies_path, param="ok", glob_pattern="*.rdf")
def test_glob(ok):
    assert isinstance(ok, Path)


@parametrize_graphs_from_glob(ontologies_path, param="graph", glob_pattern="*.rdf")
def test_graphs_glob(graph):
    assert isinstance(graph, Graph)
    assert len(graph) > 0
