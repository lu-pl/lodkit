"""Custom importer for RDF files."""

from collections.abc import Sequence
import importlib.abc
import importlib.machinery
from pathlib import Path
import sys
from types import ModuleType

from rdflib import Graph
from rdflib.util import guess_format


class RDFImporter(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    """Custom Importer for loading RDF files like modules.

    E.g. given that graph/my_graph.ttl is in the import path,
    one can do "from graph import my_graph" if RDFImporter is register
    (e.g. by calling enable_rdf_import()); this will parse my_graph.ttl
    and bind my_graph to the resulting rdflib.Graph instance.
    """

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        """Finder for RDFImporter.

        The finder checks if a given import request targets an RDF file by
        attempting to guess an RDF file format. If the imported file is an RDF file,
        the finder registers the Path to the file in the instance for the loader
        to operate on and returns a ModuleSpec indicating the importer instance as loader.
        """
        if not path:  # direct top-level graph imports are not supported
            return None

        resource_path, *_ = path
        *_, resource_name = fullname.rpartition(".")

        resource_file_path: Path | None = next(
            filter(
                lambda x: guess_format(x.suffix),
                Path(resource_path).glob(f"{resource_name}.*"),
            ),
            None,
        )

        if resource_file_path is not None:
            self.rdf_resource: Path = resource_file_path
            self.resource_name = resource_name

            return importlib.machinery.ModuleSpec(fullname, self)
        return None

    def create_module(self, spec: importlib.machinery.ModuleSpec) -> Graph:  # type: ignore
        """Parse an RDF resource and return the resulting Graph object.

        The method relies on the finder to register the Path of an RDF resource in the importer instance.
        """
        graph = Graph()
        graph.parse(str(self.rdf_resource.absolute()))

        return graph

    def exec_module(self, module: ModuleType) -> None:
        """Stub definition for the Loader ABC.

        RDFImporter shortcircuits the import maschinery by returning a Graph object from create_module;
        this means that exec_module is not meaningful for RDFImporter.

        importlib.abc.Loader raises an ImportError if a concrete Loader does not define exec_module though.
        See https://github.com/python/cpython/blob/main/Lib/importlib/_abc.py.
        """
        pass


def enable_rdf_import() -> None:
    """Invoke the module-level side effect of adding an RDFImporter instance to sys.meta_path."""

    if not any(isinstance(entry, RDFImporter) for entry in sys.meta_path):
        sys.meta_path.append(RDFImporter())
