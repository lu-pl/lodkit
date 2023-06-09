"""Inference plugins for lodkit.Graph and the plugin registry."""

from collections.abc import MutableMapping
from typing import Protocol, runtime_checkable, Self

from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_OWLRL_Semantics


@runtime_checkable
class InferencePlugin(Protocol):
    """Protocol class for all lodkit.Graph inference plugins."""

    def inference(self, graph: Graph) -> Graph:
        """Protocol method.

        Defines logic for inferencing on an rdflib.Graph intance.
        """
        ...


class OWLRLPlugin(InferencePlugin):
    """InferencePlugin for the Python owlrl inference engine.

    The combined RDFS_OWLRL_Semantics closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html.
    """

    def inference(self, graph: Graph) -> Graph:
        """Doc."""
        _graph = DeductiveClosure(RDFS_OWLRL_Semantics).expand(graph)

        return _graph


plugins: MutableMapping[str, InferencePlugin] = {
    "owlrl": OWLRLPlugin(),
}
