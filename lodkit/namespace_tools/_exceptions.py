"""Exceptions for RDF Namespace functionality."""


class OntologyNamespaceException(Exception):
    """Base exception for indicating errors during OntologyNamespace construction."""


class NamespaceDelimiterException(OntologyNamespaceException):
    """Exception indicating that determining a delimiter failed."""


class MultiOntologyHeadersException(OntologyNamespaceException):
    """Exception indicating that more than one ontology header is defined in the ontology."""


class NoOntologyHeaderException(OntologyNamespaceException):
    """Exception indicating that no ontology header is defined in the ontology."""


class MissingOntologyClassAttributeException(Exception):
    """Exception indicating that a class-level attribute 'ontology' is required but missing."""
