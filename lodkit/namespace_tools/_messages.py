"""Messages and message constructor functions for RDF Namespace exceptions/warnings."""

_namespace_delimiter_exception_message = (
    "Unable to determine namespace delimiter.\n"
    "The namespace in the ontology header does not specify a common URI entity delimiter (# or /) "
    "and attempting to retrieve a delimiter by matching declared namespaces failed.\n"
)

_no_ontology_header_message = (
    "Unable to detect ontology namespace. "
    "An ontology namespace should be defined in the ontology header.\n"
    "See https://www.w3.org/TR/owl-ref/#Ontology-def."
)

_missing_ontology_attribute_message = (
    "ClosedOntologyNamespace subclasses expect an 'ontology' class attribute.\n"
    "If dynamic namespace generation from an ontology is not needed, "
    "use rdflib.ClosedNamespace or rdflib.DefinedNamespace instead."
)


def _namespace_delimiter_warning_message(namespace: str) -> str:
    """Warning message constructor for signalling a missing entity delimiter."""
    _message = (
        f"The derived Ontology namespace '{namespace}' "
        "does not feature a common URI entity delimiter (#, /)."
    )
    return _message


def _multi_header_message(namespace_assertions: list[str]) -> str:
    """Error message constructor for MultiOntologyHeadersExceptions."""
    _message = (
        "Only a single ontology namespace permissible.\n"
        f"Found {', '.join(namespace_assertions)}"
    )
    return _message
