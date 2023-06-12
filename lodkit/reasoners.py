"""Reasoners (inference plugins) for lodkit.Graph.."""

from collections.abc import MutableMapping
from typing import Protocol, runtime_checkable

import reasonable

from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_OWLRL_Semantics, RDFS_Semantics



@runtime_checkable
class Reasoner(Protocol):
    """Protocol class for lodkit.Graph reasoners."""

    def inference(self, graph: Graph) -> Graph:
        """Logic for inferencing on an rdflib.Graph intance."""
        ...


class OWLRLReasoner(Reasoner):
    """Reasoner plugin for the Python owlrl inference engine.

    The combined RDFS_OWLRL_Semantics closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html.
    """

    _closure_type = RDFS_OWLRL_Semantics

    def inference(self, graph: Graph) -> Graph:
        """Perform inferencing on a graph."""
        _graph = DeductiveClosure(self._closure_type).expand(graph)

        return _graph


class RDFSReasoner(OWLRLReasoner):
    """Reasoner plugin for the Python owlrl inference engine.

    The RDFS closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/RDFSClosure.html.
    """

    _closure_type = RDFS_Semantics


class ReasonableReasoner(Reasoner):
    """ Reasoner plugin using the reasonable engine.

    Reasonable does OWL-RL inferencing only, RFDS entailments are not supported.
    See https://github.com/gtfierro/reasonable.
    """

    def inference(self, graph: Graph) -> Graph:
        """Perform inferencing on a graph."""
        reasoner = reasonable.PyReasoner()
        reasoner.from_graph(graph)

        entailment = iter(reasoner.reason())

        for triple in entailment:
            graph.add(triple)

        return graph








class AllegroReasoner(Reasoner):
    """InferencePlugin for the AllegroGraph inference engine."""

    ...


reasoners: MutableMapping[str, Reasoner] = {
    "owlrl": OWLRLReasoner(),
    "rdfs": RDFSReasoner(),
    "reasonable": ReasonableReasoner()
}
