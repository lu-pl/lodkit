"""Functionality for Ontology Derived Dynamic (ODD) namespaces."""

from collections.abc import Iterator
import os
from pathlib import Path
import re
from types import new_class
from typing import NoReturn, TypeAlias

from lodkit.namespace_tools._exceptions import (
    MissingOntologyClassAttributeException,
    MultiOntologyHeadersException,
    NamespaceDelimiterException,
    NoOntologyHeaderException,
    OntologyReferenceException,
)
from lodkit.namespace_tools._messages import (
    _missing_ontology_attribute_message,
    _multi_header_message,
    _namespace_delimiter_exception_message,
    _namespace_delimiter_warning_message,
    _no_ontology_header_message,
    _ontology_reference_message,
)
from loguru import logger
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import ClosedNamespace, DefinedNamespace, OWL, RDF, RDFS


_TPath: TypeAlias = str | os.PathLike
_TGraphOrPath: TypeAlias = Graph | _TPath


def _get_ontology_graph(ontology_reference: _TGraphOrPath) -> Graph:
    """Get a graph object from a _TGraphOrPath."""
    match ontology_reference:
        case Graph():
            return ontology_reference
        case ont if isinstance(ont, _TPath):
            ontology_path = Path(ontology_reference).expanduser()
            graph = Graph().parse(ontology_path)
            return graph
        case _:
            raise OntologyReferenceException(
                _ontology_reference_message(str(ontology_reference))
            )


def _delimited_namespace_p(namespace: str) -> bool:
    """Check if a namespace uses '#' or '/' as URI entity delimiters."""
    if re.search(r"(/|#)$", namespace):
        return True
    return False


def _delimiter_check_invoke_side_effects(
    namespace: str, strict_delimiters: bool
) -> None:
    """Check if namespace is delimited and invoke side effects according to strict_delimiters."""
    if not _delimited_namespace_p(namespace):
        if strict_delimiters:
            raise NamespaceDelimiterException(_namespace_delimiter_exception_message)
        else:
            logger.warning(_namespace_delimiter_warning_message(namespace))


def _get_namespace_from_ontology(
    ontology: Graph, strict_delimiters: bool = True
) -> Namespace:
    """Get the ontology namespace from an ontology graph.

    The ontology namespace is expected to be declared in the ontology header.
    See https://www.w3.org/TR/owl-ref/#Ontology-def.

    If the namespace asserted in the ontology header does not exhibit either
    a fragment or URI path entity delimiter ('#' or '/'), try to match the header namespace
    with a declared namespace which then takes precedence (regardless of delimiters).

    If a namespace does not have a #|/ delimiter, and strict=True, an error is raised;
    else the namespace is returned and a warning emitted.
    """
    _namespace_assertions = [uri for uri in ontology.subjects(RDF.type, OWL.Ontology)]

    match _namespace_assertions:
        case [URIRef()]:
            namespace_assertion = _namespace_assertions[0]
            if _delimited_namespace_p(namespace_assertion):
                namespace = Namespace(namespace_assertion)
                return namespace
            else:
                # note: case "no delimiter + not in namespaces" is not handled
                for _, ns in ontology.namespaces():
                    if namespace_assertion in ns:
                        namespace = Namespace(ns)
                        _delimiter_check_invoke_side_effects(
                            namespace, strict_delimiters
                        )
                        return namespace

        case [URIRef(), *rest]:  # noqa
            raise MultiOntologyHeadersException(
                _multi_header_message(_namespace_assertions)
            )
        case []:
            raise NoOntologyHeaderException(_no_ontology_header_message)
        case _:
            raise Exception("This should never happen.")


def _split_uri(uri: str) -> tuple[str, URIRef]:
    """Split a URI on entity delimiter."""
    *_, last = re.split("(#|/)", uri)
    return (last, URIRef(uri))


def _get_terms_from_ontology(ontology: Graph, namespace: Namespace) -> set[str]:
    """Get the names of all terms of an ontology.

    Ontology terms are terms that are
    1. in the ontology namespace and
    2. instances of either rdfs:Class, rdf:Property,
       owl:Class, owl:ObjectProperty or owl:DatatypeProperty.

    Note: Terms get set-casted to prevent duplicates on inferred graphs.
    """

    def _get_terms() -> Iterator[str]:
        _entity_classes: tuple[URIRef, ...] = (
            RDFS.Class,
            RDF.Property,
            OWL.Class,
            OWL.ObjectProperty,
            OWL.DatatypeProperty,
        )

        for s, _, o in ontology.triples((None, RDF.type, None)):
            if (o in _entity_classes) and (s in namespace):
                name, _ = _split_uri(s)
                yield name

    return set(_get_terms())


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

    def __new__(cls, ontology: _TGraphOrPath, strict_delimiters: bool = True):
        _ontology: Graph = _get_ontology_graph(ontology)
        _namespace: Namespace = _get_namespace_from_ontology(
            _ontology, strict_delimiters
        )
        _terms: set[str] = _get_terms_from_ontology(_ontology, _namespace)

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
        ontology: _TGraphOrPath = cls._get_ontology_attribute()

        _ontology: Graph = _get_ontology_graph(ontology)
        _namespace: Namespace = _get_namespace_from_ontology(_ontology)
        _terms: set[str] = _get_terms_from_ontology(_ontology, _namespace)

        cls._NS = _namespace
        cls.__annotations__ = cls.__annotations__ | {term: URIRef for term in _terms}

    @classmethod
    def _get_ontology_attribute(cls) -> _TGraphOrPath | NoReturn:
        try:
            ontology: _TGraphOrPath = cls.ontology
        except AttributeError:
            raise MissingOntologyClassAttributeException(
                _missing_ontology_attribute_message
            ) from None
        else:
            return ontology
