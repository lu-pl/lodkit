"""Pytest entry point for RDFImporter tests."""

import functools
import sys

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from lodkit import RDFImporter, enable_rdf_import


@pytest.fixture(scope="function")
def restore_meta_path():
    _sys_meta_path = sys.meta_path.copy()

    try:
        yield
    finally:
        sys.meta_path = _sys_meta_path

        for key in list(sys.modules.keys()):
            if key.startswith("test"):
                del sys.modules[key]


def test_register_importer(restore_meta_path):
    """Check if enable_rdf_import correctly registers an RDFImporter in sys.meta_path."""

    def _get_rdf_importer() -> list[RDFImporter]:
        return [
            importer for importer in sys.meta_path if isinstance(importer, RDFImporter)
        ]

    assert not _get_rdf_importer()
    enable_rdf_import()
    assert _get_rdf_importer()

    enable_rdf_import()
    enable_rdf_import()
    assert len(_get_rdf_importer()) == 1


def test_basic_rdf_import(restore_meta_path):
    """Check that RDF file import fails/succeeds before/after importer registration."""
    with pytest.raises(ImportError):
        from tests.data.graphs import ttl_graph

    enable_rdf_import()
    from tests.data.graphs import ttl_graph

    assert isinstance(ttl_graph, Graph)


def test_rdf_import_isomorphy(restore_meta_path):
    enable_rdf_import()

    from tests.data.graphs import ttl_graph, xml_graph, nt_graph, jsonld_graph

    def _isomorphic(g1: Graph, g2: Graph) -> Graph:
        """Composable Graph isomorphy predicate."""
        if isomorphic(g1, g2):
            return g2
        return Graph()

    assert functools.reduce(_isomorphic, [ttl_graph, xml_graph, nt_graph, jsonld_graph])


def test_importer_dispatch(restore_meta_path):
    """Check if RDFImporter correctly delegates to the import maschinery.

    The test attempts to import an inexistent module from a non-top-level location.

    This triggers both import maschinery delegation paths in RDFImporter:

    - top-level import -> delegate to import maschinery
    - unguessable graph format -> delegate to import maschinery

    Note that the top-level import path runs, because the import maschinery
    will attempt to import every submodule of a given module path.

    This is also the reason, why RDFImporter should be first entry in sys.meta_path here;
    else a Python importer will handle the top-level import before RDFImporter has a chance to delegate.
    """

    sys.meta_path.insert(0, RDFImporter())

    with pytest.raises(ImportError):
        from tests.data.graphs import dne  # noqa: F401
