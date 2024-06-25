"""Paths for testing."""

from importlib.resources.abc import Traversable
from importlib.resources import files


data_path: Traversable = files("tests.data")
graphs_path: Traversable = data_path / "graphs"
ontologies_path: Traversable = graphs_path / "ontologies"
fails_path = data_path / "fails"
side_effects_path = data_path / "side_effects"
