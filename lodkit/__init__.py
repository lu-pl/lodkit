"""Entry point for LODkit."""

from lodkit.namespace_tools.namespace_graph import NamespaceGraph
from lodkit.namespace_tools.ontology_namespaces import (
    ClosedOntologyNamespace,
    DefinedOntologyNamespace,
)
from lodkit.rdf_importer import RDFImporter, enable_rdf_import
from lodkit.triple_tools.triple_chain import TripleChain
from lodkit.triple_tools.ttl_constructor import (
    TPredicateObjectPair,
    TPredicateObjectPairObject,
    ttl,
)
from lodkit.uri_tools.uri_constructor import URIConstructor
