"""Reasoners (inference plugins) for lodkit.Graph.."""

from collections.abc import MutableMapping
from typing import Protocol, runtime_checkable

from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_OWLRL_Semantics


@runtime_checkable
class Reasoner(Protocol):
    """Protocol class for lodkit.Graph reasoners."""

    def inference(self, graph: Graph) -> Graph:
        """Logic for inferencing on an rdflib.Graph intance."""
        ...


class OWLRLReasoner(Reasoner):
    """Reasoner plugin for the Python owlrl inference engine

    The combined RDFS_OWLRL_Semantics closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html.
    """

    def inference(self, graph: Graph) -> Graph:
        """Perform RDFS/OWL-RL inferencing on a graph."""
        _graph = DeductiveClosure(RDFS_OWLRL_Semantics).expand(graph)

        return _graph


class AllegroReasoner(Reasoner):
    """InferencePlugin for the AllegroGraph inference engine."""

    ...


reasoners: MutableMapping[str, Reasoner] = {
    "owlrl": OWLRLReasoner(),
}
