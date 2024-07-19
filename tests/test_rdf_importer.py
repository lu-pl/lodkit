"""Tests for lodkit.rdf_importer."""

import importlib

import pytest

import lodkit
from lodkit.rdf_importer import RDFImporterException
from loguru import logger
from rdflib import Graph
from rdflib.compare import isomorphic
from tests.utils.paths import fails_path, ontologies_path, side_effects_path
from tests.utils.utils import parametrize_import_paths_from_glob


@parametrize_import_paths_from_glob(ontologies_path, param="path")
def test_rdf_importer_ontologies(path):
    """Check if an imported Graph is isomorphic with a parsed Graph."""
    import_path, path_obj = path
    imported_graph = importlib.import_module(import_path)
    parsed_graph = Graph().parse(path_obj)

    assert isomorphic(imported_graph, parsed_graph)


@parametrize_import_paths_from_glob(fails_path / "fail_imports", param="fail_path")
def test_rdf_importer_fails(fail_path):
    """Check if importing an unparsable Graph fails."""
    with pytest.raises(RDFImporterException):
        import_path, path_obj = fail_path
        importlib.import_module(import_path)


@parametrize_import_paths_from_glob(
    side_effects_path / "warning_imports", param="warning_path"
)
def test_rdf_importer_warnings(warning_path, caplog):
    """Check if a warning is emited if an empty Graph file is imported."""
    import_path, path_obj = warning_path
    importlib.import_module(import_path)

    log_msg = f"Graph parsed from '{str(path_obj)}' is empty."
    assert log_msg in caplog.text
