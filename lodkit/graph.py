"""An rdflib.Graph subclass with plugin-based inferencing capability."""

from rdflib.namespace import OWL
from rdflib import Namespace
from typing import Optional
import rdflib
import plugins


_InferencePlugin = plugins.InferencePlugin
_PluginReference = _InferencePlugin | str


class Graph(rdflib.Graph):
    """Subclass of rdflib.Graph with plugin-based inferencing capability."""

    def __init__(self,
                 plugin: Optional[_PluginReference] = None,
                 *args, **kwargs) -> None:

        self.plugin: _PluginReference = plugin
        super().__init__(*args, **kwargs)

    def _resolve_plugin(self,
                        plugin: _PluginReference) -> _InferencePlugin:
        """Get an InferencePlugin instance from a _PluginReference."""
        if isinstance(plugin, str):
            return plugins.plugins[plugin]

        elif isinstance(plugin, _InferencePlugin):
            return plugin

        raise Exception("InferencePlugin not seizable.")

    def inference(self,
                  plugin: Optional[_PluginReference] = None) -> rdflib.Graph:
        """Perform inferencing according to an InferencePlugin."""

        # get an actual InferencePlugin
        _plugin_reference: _PluginReference = plugin or self.plugin
        _plugin: _InferencePlugin = self._resolve_plugin(_plugin_reference)

        # call the reasoner
        return _plugin.inference(self)


# first tests
# q: is (ex.obj ex.inverse ex.subj) in the graph?
# a: yet, it is! :)

ex = Namespace("http://example.org/")

graph = Graph()
graph.add((ex.subj, ex.pred, ex.obj))
graph.add((ex.inverse, OWL.inverseOf, ex.pred))

print(len(graph))
print((ex.obj, ex.inverse, ex.subj) in graph)
# print(graph.serialize())

# graph.inference(plugin="owlrl")
graph.inference(plugin=plugins.OWLRLPlugin())
print(len(graph))
print((ex.obj, ex.inverse, ex.subj) in graph)
# print(graph.serialize())
