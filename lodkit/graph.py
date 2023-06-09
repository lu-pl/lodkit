"""lodkit.Graph, an rdflib.Graph subclass with plugin-based inferencing capability."""

from typing import Optional

import rdflib

import plugins


_PluginReference = Optional[plugins.InferencePlugin | str]


class Graph(rdflib.Graph):
    """Subclass of rdflib.Graph with plugin-based inferencing capability."""

    def __init__(self, plugin: _PluginReference = None, *args, **kwargs):
        """Optionally add the plugin parameter to the Graph signature."""
        self.plugin: _PluginReference = plugin

        super().__init__(*args, **kwargs)

    def _resolve_plugin(self,
                        plugin: _PluginReference) -> plugins.InferencePlugin:
        """Get an InferencePlugin instance from a _PluginReference."""
        if isinstance(plugin, str):
            return plugins.plugins[plugin]

        elif isinstance(plugin, plugins.InferencePlugin):
            return plugin

        raise Exception("InferencePlugin not seizable.")

    def inference(self, plugin: _PluginReference = None) -> rdflib.Graph:
        """Perform inferencing according to an InferencePlugin."""
        # get an actual InferencePlugin
        _plugin_reference: _PluginReference = plugin or self.plugin
        _plugin: plugins.InferencePlugin = self._resolve_plugin(_plugin_reference)

        # call the reasoner
        return _plugin.inference(self)


#### first tests
## q: is (ex.obj ex.inverse ex.subj) in the graph?
## a: yet, it is! :)

from rdflib import Namespace
from rdflib.namespace import OWL

ex = Namespace("http://example.org/")

graph = Graph()
graph.add((ex.subj, ex.pred, ex.obj))
graph.add((ex.inverse, OWL.inverseOf, ex.pred))

print(graph.serialize())

graph.inference(plugin="owlrl")
print(graph.serialize())
