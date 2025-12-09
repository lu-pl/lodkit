"""Entry point for LODkit."""

from lodkit.namespace_tools.namespace_graph import NamespaceGraph
from lodkit.namespace_tools.ontology_namespaces import (
    ClosedOntologyNamespace,
    DefinedOntologyNamespace,
)
from lodkit.rdf_importer import RDFImporter, enable_rdf_import
from lodkit.triple_tools.triple_chain import TripleChain
from lodkit.triple_tools.ttl_constructor import (
    _TPredicateObjectPair,
    _TPredicateObjectPairObject,
    ttl,
)
from lodkit.uri_tools.uribase import uribase
from lodkit.uri_tools.uriclass import make_uriclass, uriclass
from lodkit.uri_tools.utils import (
    URIConstructorFactory,
    generate_uri_hash,
    generate_uri_id_segment,
    mkuri_factory,
)
