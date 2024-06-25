"""rdflib.Graph format options."""

from collections.abc import Iterator
from typing import Annotated

from rdflib.plugin import plugins
from rdflib.serializer import Serializer


graph_serialize_formats_options: Annotated[
    list[str], "rdflib.Graph.serialize format options (i.e. RDFLib plugin names)."
] = [plugin.name for plugin in plugins() if plugin.kind == Serializer]


quad_format_options: Annotated[
    list[str], "rdflib.Graph.serialize options for quad formats."
] = [
    "application/n-quads",
    "nquads",
    "application/trix",
    "trix",
    "application/trig",
    "trig",
]

triple_format_options: Annotated[
    list[str], "rdflib.Graph.serialize options for quad formats."
] = [
    _format
    for _format in graph_serialize_formats_options
    if _format not in quad_format_options
]
