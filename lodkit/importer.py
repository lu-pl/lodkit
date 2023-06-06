"""Custom importer for RDF files.
"""

# from importlib.abc import Finder, Loader
from importlib.machinery import ModuleSpec

import pathlib
import sys

from rdflib import Graph


class RDFImporter:
    """Custom importer; allows to import RDF files as if they were modules.

    E.g. 'import some_rdf' looks for some_rdf.() in the import path,
    parses it into an rdflib.Graph instance and makes it available in the module namespace.
    """

    def __init__(self, rdf_path):
        self.rdf_path = rdf_path


    @classmethod
    def find_spec(cls, name, path, target=None):

        *_, module_name = name.rpartition(".")

        directories = sys.path if path is None else path

        # print("DEBUG: ", directories)

        for directory in directories:

            rdf_paths = pathlib.Path(directory).glob(f"{module_name}.*")

            for path in rdf_paths:
                if path.exists():
                    return ModuleSpec(name, cls(path))


    def create_module(self, spec):
        graph = Graph().parse(self.rdf_path)
        return graph

    def exec_module(self, module):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.rdf_path)!r})"


# module level side-effect
sys.meta_path.append(RDFImporter)
