"""Custom importer for RDF files.
"""

# from importlib.abc import Finder, Loader
from importlib.machinery import ModuleSpec

import pathlib
import re
import sys

from rdflib import Graph


#### todo: make this general (try: Graph.parse)

class RDFImporter:
    """Custom RDF importer. i

    Allows to import RDF files as if they were modules.

    E.g. 'import some_rdf' looks for 'some_rdf.*' in the import path,
    parses it into an rdflib.Graph instance and makes it available in the module namespace.
    """

    def __init__(self, rdf_path):
        self.rdf_path = rdf_path


    # maybe use spec_from_loader?
    @classmethod
    def find_spec(cls, name, path, target=None):

        directories = sys.path if path is None else path

        for directory in directories:
            # trust that something that rdflib.Graph.parse can handle is provided
            # is this naive? better check for rdf serialization extensions?
            # (this way also rdf files named like Python modules could be passed)

            for f in pathlib.Path(directory).glob(f"{name}.*"):
                rdf_path = f.absolute()
                return ModuleSpec(name, cls(rdf_path))

    def create_module(self, spec):
        graph = Graph().parse(self.rdf_path)
        return graph

    def exec_module(self, module):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.rdf_path)!r})"


# module level side-effect
sys.meta_path.append(RDFImporter)
