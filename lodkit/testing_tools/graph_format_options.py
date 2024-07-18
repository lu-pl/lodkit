"""rdflib.Graph format options."""

from collections.abc import Iterator
from typing import Annotated

from rdflib.parser import Parser
from rdflib.plugin import plugins
from rdflib.serializer import Serializer


graph_serialize_format_options: Annotated[
    list[str],
    "rdflib.Graph.serialize format options (i.e. RDFLib serialize plugin names).",
] = [plugin.name for plugin in plugins() if plugin.kind == Serializer]

graph_parse_format_options: Annotated[
    list[str], "rdflib.Graph.parse format options (i.e. RDFLib parse plugin names)."
] = [plugin.name for plugin in plugins() if plugin.kind == Parser]

# note: is there an easy and reliable way to formally determine quad plugins?
_quad_formats = [
    "nquads",
    "application/n-quads",
    "trix",
    "application/trix",
    "trig",
    "application/trig",
]

quad_serialize_format_options: Annotated[
    list[str], "rdflib.Graph.serialize options for quad formats."
] = _quad_formats

triple_serialize_format_options: Annotated[
    list[str], "rdflib.Graph.serialize options for triple formats."
] = [
    _format
    for _format in graph_serialize_format_options
    if _format not in quad_serialize_format_options
]

quad_parse_format_options: Annotated[
    list[str], "rdflib.Graph.parse options for quad formats."
] = _quad_formats

triple_parse_format_options: Annotated[
    list[str], "rdflib.Graph.parse options for triple formats."
] = [
    _format
    for _format in graph_parse_format_options
    if _format not in quad_parse_format_options
]


def get_parse_format_from_serialize_format(parse_option: str) -> str:
    """Get the corresponding parse format given a serialization format."""
    match parse_option:
        case "pretty-xml":
            return "xml"
        case "longturtle":
            return "ttl"
        case _:
            return parse_option
