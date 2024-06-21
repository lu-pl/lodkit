"""Import entry point for LODkit."""

import sys

from lodkit.lod_types import (
    _GraphFormatOptions,
    _RDFTerm,
    _Triple,
    _TripleBNodeObject,
    _TripleBNodeObject,
    _TripleObject,
    _TripleSubject,
    _TripleURIObject,
)
from lodkit.namespace_tools.namespace_graph import NamespaceGraph
from lodkit.namespace_tools.ontology_namespaces import (
    ClosedOntologyNamespace,
    DefinedOntologyNamespace,
)
from lodkit.rdf_importer import RDFImporter
from lodkit.triple_tools.ttl import plist, ttl
from lodkit.uri_tools.uribase import uribase
from lodkit.uri_tools.uriclass import make_uriclass, uriclass
from lodkit.uri_tools.utils import (
    URIConstructorFactory,
    generate_uri_hash,
    generate_uri_id_segment,
    mkuri_factory,
)


# module level side-effect
sys.meta_path.append(RDFImporter)
