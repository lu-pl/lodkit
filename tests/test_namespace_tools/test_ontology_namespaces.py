""""""

from collections.abc import Iterator
from importlib.resources.abc import Traversable

import pytest

from hypothesis import given
from tests.utils.strategies.ns_strategies import public_variable_names
from lodkit import ClosedOntologyNamespace
from lodkit.namespace_tools.ontology_namespaces import (
    _get_namespace_from_ontology,
    _get_terms_from_ontology,
)
from rdflib import Graph
from tests.utils.paths import ontologies_path


_ontologies: list[Traversable] = list(ontologies_path.iterdir())


@pytest.mark.parametrize("ontology_path", _ontologies)
def test_closed_ontology_namespace_from_path(ontology_path):
    """Define a ClosedOntologyNamespace from a path and check for all terms."""
    closed_ontology_namespace = ClosedOntologyNamespace(ontology_path)

    _graph = Graph().parse(ontology_path)
    _namespace = _get_namespace_from_ontology(_graph)
    _terms = _get_terms_from_ontology(_graph, _namespace)

    for term in _terms:
        assert getattr(closed_ontology_namespace, term)


@pytest.mark.parametrize("ontology_path", _ontologies)
def test_closed_ontology_namespace_from_graph(ontology_path):
    """Define a ClosedOntologyNamespace from a graph and check for all terms."""
    _graph = Graph().parse(ontology_path)
    closed_ontology_namespace = ClosedOntologyNamespace(_graph)

    _namespace = _get_namespace_from_ontology(_graph)
    _terms = _get_terms_from_ontology(_graph, _namespace)

    for term in _terms:
        assert getattr(closed_ontology_namespace, term)


@given(public_variable_names)
@pytest.mark.parametrize("ontology_path", _ontologies)
def test_closed_ontology_namespace_unknown_term_fail(ontology_path, variable_name):
    """Check that random attributes are not in an ClosedOntologyNamespace (flaky)."""
    closed_ontology_namespace = ClosedOntologyNamespace(ontology_path)

    with pytest.raises(AttributeError):
        getattr(closed_ontology_namespace, variable_name)
