from types import MappingProxyType

from lodkit.types import GraphParseSource
from rdflib import Graph, URIRef
from rdflib.query import Result


class NoSolutionException(Exception): ...


class EmptySolutionException(Exception): ...  # pragma: no cover


class ClosedOntologyNamespace:
    """Ontology-based Namespace constructor.

    ClosedOntologyNamespace allows constructing a namespace
    based on an Ontology or generally an RDF graph source.

    Given a lodkit.types.GraphParseSource or an rdflib.Graph,
    the source is queried for RDF class and property definition assertions.
    RDF term names are extracted by splitting the last IRI segment delimited by
    '#', '/' or ':' and  matching name/IRI pairs are registered in the namespace mapping.

    Namespace members are accessible as both attributes and items of a given
    `ClosedOntologyNamespace` instance, i.e. attribute and item access is routed
    to `ClosedOntologyNamespace.mapping`. For dictionary operations over the namespace mapping,
    the public `ClosedOntologyNamespace.mapping` can be accessed directly.

    In the case of RDF term names conflicting with class namespace names,
    the class namespace names take precedence for attribute access;
    conflicting RDF terms are still accessible via item lookup
    or through the `ClosedOntologyNamespace.mapping` proxy.

    """

    _query = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix owl: <http://www.w3.org/2002/07/owl#>

    select distinct ?name ?uri
    where {
    values ?type {
      rdfs:Class
      owl:Class

      rdf:Property
      owl:ObjectProperty
      owl:DatatypeProperty
      owl:AnnotationProperty

      owl:NamedIndividual
    }

    ?uri a ?type .
    filter (isIRI(?uri))

    bind (replace(str(?uri), "^.*[#/:]", "") AS ?name)
    filter (?name != "")
    }
    """

    def __init__(self, source: GraphParseSource | Graph, *parse_args, **parse_kwargs):
        self.source = source

        graph: Graph = (
            self.source
            if isinstance(self.source, Graph)
            else Graph().parse(source=self.source, *parse_args, **parse_kwargs)
        )
        sparql_result: Result = graph.query(self._query)

        self.mapping: MappingProxyType[str, URIRef] = self._get_uris(
            sparql_result=sparql_result
        )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<{self.__class__.__name__} source={self.source!r}>"

    def __getattr__(self, value):
        return self[value]

    def __getitem__(self, key: str) -> URIRef:
        try:
            return self.mapping[key]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{key}'."
            )

    def _get_uris(self, sparql_result: Result) -> MappingProxyType[str, URIRef]:
        _bindings = sparql_result.bindings

        match _bindings:
            case []:
                raise NoSolutionException()
            case [{**items}] if not items:  # pragma: no cover (unreachable)
                raise EmptySolutionException()
            case _:
                return MappingProxyType(
                    {
                        str(binding["name"]): binding["uri"]  # type: ignore
                        for binding in _bindings
                    }
                )
