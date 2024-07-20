"""Custom importer for RDF files."""

from importlib.machinery import ModuleSpec
import pathlib
import sys

from loguru import logger
from rdflib import Graph
from rdflib.plugin import PluginException
from rdflib.exceptions import ParserError


class RDFImporterException(Exception):
    """Exception indicating that RDFImporter ran but failed to import a graph."""


class RDFImporter:
    """Importer for directly importing RDF files as if they were modules.

     The importer works by Searching the PYTHONPATH for RDF files
     and parsing them into rdflib.Graph instances.

     Note that RDFImporter is added to the meta_path in lodkit.__init__
     so this functionality is available as soon as any lodkit import runs.

    Examples:

        # assuming e.g. 'graphs/some_graph.ttl' exists in the import path

        import lodkit
        from graphs import some_graph

        type(some_graph)  # <class 'rdflib.graph.Graph'>
    """

    def __init__(self, rdf_path):
        self.rdf_path = rdf_path

    @classmethod
    def find_spec(cls, name, path, target=None):
        *_, module_name = name.rpartition(".")
        directories = sys.path if path is None else path

        for directory in directories:
            # don't check for RDF extensions, handle PluginException instead
            rdf_paths = pathlib.Path(directory).glob(f"{module_name}.*")

            for path in rdf_paths:
                if path.exists():
                    return ModuleSpec(name, cls(path))  # type: ignore

    def create_module(self, spec):
        try:
            graph = Graph().parse(self.rdf_path)
            if not graph:
                logger.warning(f"Graph parsed from '{self.rdf_path}' is empty.")
        except Exception as e:
            raise RDFImporterException(
                f"Importing graph failed due to '{e.__class__.__name__}' (see stack trace)."
            )
        else:
            return graph

    def exec_module(self, module):
        pass
