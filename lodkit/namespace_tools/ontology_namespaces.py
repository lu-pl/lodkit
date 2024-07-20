"""Functionality for Ontology Derived Dynamic (ODD) namespaces."""

from lodkit.namespace_tools._exceptions import MissingOntologyClassAttributeException
from lodkit.namespace_tools._messages import _missing_ontology_attribute_message
from lodkit.namespace_tools.utils import (
    _TGraphParseSource,
    _get_namespace_from_ontology,
    _get_ontology_graph,
    _get_terms_from_ontology,
)
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import ClosedNamespace, DefinedNamespace


class ClosedOntologyNamespace(ClosedNamespace):
    """Ontology-derived ClosedNamespace.

    Namespace members are determined by parsing an Ontology for entities.
    Trying to access an undefined member results in an AttributeError.

    rdflib.ClosedNamespaces are meant to be instantiated,
    so this extension is implemented to take an ontology argument upon instantiation.
    See https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.ClosedNamespace.

    Example:

        crm = ClosedOntologyNamespace(ontology="./CIDOC_CRM_v7.1.3.ttl")
        crm.E39_Actor   # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Actor')
        crm.E39_Author  # AttributeError
    """

    def __new__(cls, ontology: _TGraphParseSource, strict_delimiters: bool = True):
        _ontology: Graph = _get_ontology_graph(ontology)
        _namespace: Namespace = _get_namespace_from_ontology(
            _ontology, strict_delimiters
        )
        _terms: list[str] = _get_terms_from_ontology(_ontology, _namespace)

        return super().__new__(cls, uri=_namespace, terms=_terms)


class DefinedOntologyNamespace(DefinedNamespace):
    """Ontology-derived DefinedNamespace.

    Namespace members are determined by parsing an Ontology for entities.
    Trying to access an undefined member emits a UserWarning.

    rdflib.DefinedNameSpace is meant to be extended,
    parameters for namespace generation are set as class-level attributes in the subclass;
    so this extension is implemented to expect an 'ontology' class attribute.
    See https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.namespace.html#rdflib.namespace.DefinedNamespace.

    Example:

        class crm(DefinedOntologyNamespace):
            ontology = "./CIDOC_CRM_v7.1.3.ttl"

        crm.E39_Actor   # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Actor')
        crm.E39_Author  # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Author') + UserWarning
    """

    def __init_subclass__(cls) -> None:
        ontology: _TGraphParseSource = cls._get_ontology_attribute()

        _ontology: Graph = _get_ontology_graph(ontology)
        _namespace: Namespace = _get_namespace_from_ontology(_ontology)
        _terms: list[str] = _get_terms_from_ontology(_ontology, _namespace)

        cls._NS = _namespace
        cls.__annotations__ = cls.__annotations__ | {term: URIRef for term in _terms}

    @classmethod
    def _get_ontology_attribute(cls) -> _TGraphParseSource:
        try:
            ontology: _TGraphParseSource = cls.ontology
        except AttributeError:
            raise MissingOntologyClassAttributeException(
                _missing_ontology_attribute_message
            ) from None
        else:
            return ontology
