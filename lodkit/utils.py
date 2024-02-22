"""LODKit utilities."""

import hashlib

from collections.abc import Callable, Iterator, Iterable
from itertools import repeat
from functools import partial
from typing import Self, Optional
from types import SimpleNamespace
from uuid import uuid4

from rdflib import BNode, Graph, URIRef, Namespace
from lodkit.types import _TripleObject, _Triple


class ttl:
    """Triple/graph constructor implementing a ttl-like interface.

    The callable interface aims to provide a Python representation of
    Turtle predicate and object list syntax (';' and ',').
    See https://www.w3.org/TR/rdf12-turtle/#predicate-lists and
    https://www.w3.org/TR/rdf12-turtle/#object-lists.

    Example:

    triples = ttl(
        # 1. subject
        URIRef("https://subject.uri"),
        # 2. predicate lists
        # 2.1 predicate + object list
        (RDF.type, (lrm["F3_Manifestation"], crmdig["D1_Digital_Object"])),
        # 2.2 predicate + blank node object
        (crm["P1_is_identified_by"], [
            (RDF.type, crm["E41_Appellation"]),
            (crm["P190_has_symbolic_content"], Literal("Have more fun!"))
        ])
    )

    to_graph generates and returns an rdflib.Graph instance.
    """

    def __init__(self,
                 uri: URIRef,
                 *predicate_object_pairs: tuple[URIRef, _TripleObject | list | Self],
                 graph: Optional[Graph] = None):
        """Initialize a plist object."""
        self.uri = uri
        self.predicate_object_pairs = predicate_object_pairs
        self.graph = Graph() if graph is None else graph
        self._iter = iter(self)

    def __iter__(self) -> Iterator[_Triple]:
        """Generate an iterator of tuple-based triple representations."""
        for pred, obj in self.predicate_object_pairs:
            match obj:
                case ttl():
                    yield (self.uri, pred, obj.uri)
                    yield from obj
                case list() | Iterator():
                    _b = BNode()
                    yield (self.uri, pred, _b)
                    yield from ttl(_b, *obj)
                case tuple():
                    _object_list = zip(repeat(pred), obj)
                    yield from ttl(self.uri, *_object_list)
                case _:
                    yield (self.uri, pred, obj)

    def __next__(self) -> _Triple:
        """Return the next triple from the iterator."""
        return next(self._iter)

    def to_graph(self) -> Graph:
        """Generate a graph instance."""
        for triple in self:
            self.graph.add(triple)
        return self.graph


class plist(ttl):
    """Deprecated alias to ttl.

    This is for backwards api compatibility only.
    Since ttl also implements Turtle object lists now,
    refering to the class as "plist" is inaccurate/misleading.
    """


def genhash(input: str,
            length: int | None = 10,
            hash_function: Callable = hashlib.sha256) -> str:
    """Generate a truncated URL-safe string hash.

    Pass length=None for an untruncated hash.
    """
    _hash = hash_function(input.encode('utf-8')).hexdigest()
    return _hash[:length]


def mkuri_path(
        hash_value: str | None = None,
        length: int | None = 10,
        hash_function: Callable = hashlib.sha256,
        uuid_function: Callable = uuid4
) -> str:
    """Generate a URI path.

    If a hash value is given, the path is generated using
    a hash function, else the path is generated using a uuid.
    """
    _path: str = (
        str(uuid_function()) if hash_value is None
        else genhash(
                hash_value,
                length=length,
                hash_function=hash_function
        )
    )
    return _path

def mkuri_factory(
        namespace: Namespace,
        path_callback: Callable = mkuri_path
) -> Callable:
    """Factory for generating URI constructor callables.

    The generated callable takes args and kwargs
    which are passed to the path_callback.
    """
    return lambda *args, **kwargs: namespace[path_callback(*args, **kwargs)]


class URINamespace(SimpleNamespace):
    """A SimpleNamespace for binding URIRefs to names.

    Example:
    uris = URINamespace(
        namespace=Namespace("https://namespace.test"),
        names = (
            "test_uri",
            ("hashed_uri", "hash_value")
        )
    )

    print(uris.test_uri)
    print(uris.hashed_uri)
    """
    def __init__(
            self,
            *,
            namespace: str | Namespace,
            names: Iterable[str | tuple[str, str]],
            path_callback: Callable = mkuri_path,
            **kwargs
    ) -> None:
        self.namespace = (
            Namespace(namespace)
            if isinstance(namespace, str)
            else namespace
        )
        self._names = names
        self._path_callback = path_callback
        self._kwargs = kwargs

        self._uris: dict[str, URIRef] = self._generate_uri_mapping()
        super().__init__(**self._uris)


    def _generate_uri_mapping(self) -> dict[str, URIRef]:
        _mkuri = mkuri_factory(
            self.namespace,
            partial(self._path_callback, **self._kwargs)
        )

        def _uris():
            for name in self._names:
                match name:
                    case str():
                        yield name, _mkuri()
                    case tuple():
                        _name, _hash_value = name
                        yield _name, _mkuri(_hash_value)
                    case _:
                        raise Exception("Args must be of type str | tuple[str, str]")

        return dict(_uris())
