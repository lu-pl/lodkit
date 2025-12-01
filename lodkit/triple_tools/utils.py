"""LODKit triple tools utils."""

from collections.abc import Iterable
import warnings

from lodkit import _Triple
from rdflib import Graph


class _ToGraphMixin:
    """Mixin that adds a to_graph method for generating graphs from Iterable[_Triple] objects."""

    def to_graph(self: Iterable[_Triple], graph: Graph | None = None) -> Graph:
        _graph: Graph = Graph() if graph is None else graph

        for triple in self:
            _graph.add(triple)

        if not _graph:
            msg = f"Graph object '{_graph}' is empty. This might indicate an exhausted iterator."
            warnings.warn(msg)

        return _graph
