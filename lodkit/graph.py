"""An rdflib.Graph subclass with plugin-based inferencing capability."""

from rdflib.namespace import OWL
from rdflib import Namespace
from typing import Optional
import rdflib
import reasoners


_Reasoner = reasoners.Reasoner
_ReasonerReference = _Reasoner | str


class Graph(rdflib.Graph):
    """Subclass of rdflib.Graph with inferencing capability."""

    def __init__(self,
                 reasoner: Optional[_ReasonerReference] = None,
                 *args, **kwargs) -> None:

        self.reasoner = reasoner
        super().__init__(*args, **kwargs)

    def _resolve_reasoner(self,
                        reasoner: _ReasonerReference) -> _Reasoner:
        """Get an actual _Reasoner instance from a _ReasonerReference."""
        if isinstance(reasoner, str):
            return reasoners.reasoners[reasoner]

        elif isinstance(reasoner, _Reasoner):
            return reasoner

        raise Exception("Reasoner not seizable.")

    def inference(self,
                  reasoner: Optional[_ReasonerReference] = None) -> rdflib.Graph:
        """Perform inferencing according to an InferencePlugin."""

        # get an actual InferencePlugin
        _reasoner_reference: _ReasonerReference = reasoner or self.reasoner
        _reasoner: _Reasoner = self._resolve_reasoner(_reasoner_reference)

        # call the reasoner
        return _reasoner.inference(self)



##################################################
ex = Namespace("http://example.org/")

graph = Graph()
graph.add((ex.subj, ex.pred, ex.obj))
graph.add((ex.inverse, OWL.inverseOf, ex.pred))

print(len(graph))
print((ex.obj, ex.inverse, ex.subj) in graph)
# print(graph.serialize())

# graph.inference(reasoner="owlrl")
# graph.inference(reasoner="reasonable")
# graph.inference(reasoner=reasoners.OWLRLReasoner())
print(len(graph))
print((ex.obj, ex.inverse, ex.subj) in graph)
# print(graph.serialize())
