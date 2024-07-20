""""""

from importlib.resources.abc import Traversable

from hypothesis import strategies as st
from lodkit import ClosedOntologyNamespace
from lodkit.namespace_tools._exceptions import NamespaceDelimiterException
from lodkit.namespace_tools.utils import (
    MultiOntologyHeadersException,
    NoOntologyHeaderException,
    _get_namespace_from_ontology,
    _get_terms_from_ontology,
)
import pytest
from rdflib import Graph
from tests.utils.paths import fail_ontologies_path, ontologies_path
from tests.utils.utils import parametrize_paths_from_glob


_ontologies: list[Traversable] = list(
    obj for obj in ontologies_path.iterdir() if obj.is_file()
)


@pytest.mark.parametrize("ontology_path", _ontologies)
def test_closed_ontology_namespace_from_path(ontology_path):
    """Initialize a ClosedOntologyNamespace from a path and check for all terms."""
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


@pytest.mark.parametrize("ontology_path", _ontologies)
def test_closed_ontology_namespace_unknown_term_fail(ontology_path):
    """Check that an unknown attribute fails when requested from a ClosedOntologyNamespace."""
    closed_ontology_namespace = ClosedOntologyNamespace(ontology_path)

    with pytest.raises(AttributeError):
        getattr(closed_ontology_namespace, "does_not_exist")


@parametrize_paths_from_glob(
    fail_ontologies_path / "delimiter_fails", param="fail_ontology"
)
def test_closed_ontology_namespace_delimiter_side_effects_exception(fail_ontology):
    """Check if an undelimited namespace raises an exception if strict_delimiters=True."""

    with pytest.raises(NamespaceDelimiterException):
        closed_ontology_namespace = ClosedOntologyNamespace(
            fail_ontology, strict_delimiters=True
        )


@parametrize_paths_from_glob(
    fail_ontologies_path / "delimiter_fails", param="fail_ontology"
)
def test_closed_ontology_namespace_delimiter_side_effects_warning(
    fail_ontology, caplog
):
    """Check if an undelimited namespace emits a warning if strict_delimiters=False."""
    closed_ontology_namespace = ClosedOntologyNamespace(
        fail_ontology, strict_delimiters=False
    )
    log_message = (
        f"The derived Ontology namespace '{closed_ontology_namespace.uri}' "
        "does not feature a common URI entity delimiter (#, /)."
    )

    assert log_message in caplog.text


def test_closed_ontology_multi_header_fail():
    """Check if a MultiOntologyHeadersException is raised."""
    fail_ontology_path = fail_ontologies_path / "header_fails/multiple_headers.ttl"
    with pytest.raises(MultiOntologyHeadersException):
        closed_ontology_namespace = ClosedOntologyNamespace(fail_ontology_path)


def test_closed_ontology_no_header_fail():
    """Check if a NoOntologyHeadersException is raised."""
    fail_ontology_path = fail_ontologies_path / "header_fails/no_header_cidoc.ttl"
    with pytest.raises(NoOntologyHeaderException):
        closed_ontology_namespace = ClosedOntologyNamespace(fail_ontology_path)
