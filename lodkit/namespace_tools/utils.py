"""Utility functions for Ontology Namespaces."""

from collections.abc import Iterator
import os
from pathlib import Path, PurePath
import re
from typing import Annotated, IO, TextIO, TypeAlias, cast

from lodkit.namespace_tools._exceptions import (
    MultiOntologyHeadersException,
    NamespaceDelimiterException,
    NoOntologyHeaderException,
)
from lodkit.namespace_tools._messages import (
    _multi_header_message,
    _namespace_delimiter_exception_message,
    _namespace_delimiter_warning_message,
    _no_ontology_header_message,
)
from loguru import logger
from rdflib import Graph, Namespace, OWL, RDF, RDFS, URIRef
from rdflib.parser import InputSource


_TGraphParseSource: Annotated[
    TypeAlias,
    """Source parameter type for rdflib.Graph.parse.
    This is the exact type defined in RDFLib.
    """,
] = (
    IO[bytes] | TextIO | InputSource | str | bytes | PurePath
)


def _get_ontology_graph(ontology_reference: Graph | _TGraphParseSource) -> Graph:  # type: ignore
    """Get a graph object from a _TGraphOrPath."""
    graph = (
        ontology_reference
        if isinstance(ontology_reference, Graph)
        else Graph().parse(source=ontology_reference)
    )

    return graph


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


def _resolve_namespace_from_namespace_assertion(
    namespace_assertion: Namespace, ontology: Graph, strict_delimiters: bool
) -> Namespace:
    """Helper for _get_namespace_from_ontology.

    Resolve a namespace from"""
    if _delimited_namespace_p(namespace_assertion):
        namespace = Namespace(namespace_assertion)
        return namespace
    else:
        for _, ns in ontology.namespaces():
            if namespace_assertion in ns:
                namespace = Namespace(ns)
                break
        else:
            namespace = namespace_assertion

        _delimiter_check_invoke_side_effects(namespace, strict_delimiters)
        return namespace


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
    # cast: RDFLib triple subjects are typed as graph._SubjectType/terms.Node
    namespace_assertions = cast(
        list[Namespace], [uri for uri in ontology.subjects(RDF.type, OWL.Ontology)]
    )

    match namespace_assertions:
        case [URIRef()]:
            namespace_assertion = namespace_assertions[0]
            namespace = _resolve_namespace_from_namespace_assertion(
                namespace_assertion=namespace_assertion,
                ontology=ontology,
                strict_delimiters=strict_delimiters,
            )
            return namespace
        case [URIRef(), *_]:
            raise MultiOntologyHeadersException(
                _multi_header_message(namespace_assertions)
            )
        case []:
            raise NoOntologyHeaderException(_no_ontology_header_message)
        case _:  # pragma: no cover
            raise Exception("This should never happen.")


def _split_uri(uri: str) -> tuple[str, URIRef]:
    """Split a URI on entity delimiter."""
    *_, last = re.split("(#|/)", uri)
    return (last, URIRef(uri))


def _get_terms_from_ontology(ontology: Graph, namespace: Namespace) -> list[str]:
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
            # cast: s is a URIRef/str and has special behavior for containment checks against Namesapce
            s = cast(URIRef, s)
            if (o in _entity_classes) and (s in namespace):
                name, _ = _split_uri(s)
                yield name

    return list(set(_get_terms()))
