"""Tests for lodkit.DefinedOntologyNamespace."""

from inspect import get_annotations

from hypothesis import given, settings
from lodkit import DefinedOntologyNamespace
from lodkit.namespace_tools.ontology_namespaces import (
    MissingOntologyClassAttributeException,
)
from lodkit.namespace_tools.utils import _TGraphParseSource, _get_terms_from_ontology
import pytest
from rdflib import Graph, URIRef
from tests.utils.paths import ontologies_path
from tests.utils.strategies.ns_strategies import public_variable_names
from tests.utils.utils import parametrize_paths_from_glob


owl = ontologies_path / "owl.ttl"


def _defined_ontology_class_factory(
    ontology_reference: _TGraphParseSource,
) -> type[DefinedOntologyNamespace]:
    """Construct a DefinedOntologyNamespace class from an ontology_reference."""
    defined_ontology_class = type(
        "TestingDefinedOntologyNamespace",
        (DefinedOntologyNamespace,),
        {"ontology": ontology_reference},
    )

    return defined_ontology_class


def _get_terms_from_defined_namespace(namespace_cls: type) -> list[str]:
    """Get terms from a DefinedNamespace."""
    return [
        name for name, uri in get_annotations(namespace_cls).items() if uri == URIRef
    ]


@parametrize_paths_from_glob(ontologies_path, param="ontology_path")
def test_defined_ontology_namespace_missing_ontology_reference(ontology_path):
    """Check if all terms from a defined namespace are in the Ontology."""
    defined_ontology_class = _defined_ontology_class_factory(ontology_path)
    graph = Graph().parse(ontology_path)

    defined_terms = _get_terms_from_defined_namespace(defined_ontology_class)

    for term in defined_terms:
        assert term in _get_terms_from_ontology(graph, defined_ontology_class._NS)


def test_defined_ontology_namespace_containment():
    with pytest.raises(MissingOntologyClassAttributeException):

        class TestingDefinedOntologyNamespace(DefinedOntologyNamespace):
            pass
