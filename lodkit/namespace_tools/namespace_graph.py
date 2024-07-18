"""NamespaceGraph: rdflib.Graph extension for convenient namespace binding."""

from typeguard import check_type

from rdflib import Graph, Namespace, URIRef


class NamespaceGraph(Graph):
    """Simple rdflib.Graph subclass for easy and convenient namespace binding.

    Public class-level attributes of NamespaceGraph subclasses are interpreted as namespaces
    and automatically bound for instances of that graph class.

    Example:

        class CLSGraph(NamespaceGraph):
            crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
            crmcls = Namespace("https://clscor.io/ontologies/CRMcls/")
            clscore = Namespace("https://clscor.io/entity/")

        graph = CLSGraph()

        ns_check: bool = all(
            ns in map(lambda x: x[0], graph.namespaces())
            for ns in ("crm", "crmcls", "clscore")
        )

        print(ns_check)  # True
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for name, namespace in self._bindings.items():
            self.bind(name, namespace)

    def __init_subclass__(cls) -> None:
        cls._bindings = {
            name: Namespace(namespace)
            for name, namespace in cls.__dict__.items()
            if not name.startswith("_")
            # URIRef/Namespace are str subclasses, but this gives better error messages
            and check_type(namespace, str | URIRef | Namespace)
        }
