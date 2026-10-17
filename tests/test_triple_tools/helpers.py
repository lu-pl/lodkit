from rdflib import Graph
from rdflib.compare import to_canonical_graph


def canonical_triples(graph: Graph) -> list[str]:
    """Serialize a graph to a sorted list of canonical N-Triples lines."""
    return sorted(to_canonical_graph(graph).serialize(format="nt").splitlines())
