"""LODKit URIConstructor functionality."""

from hashlib import sha256
from uuid import uuid4

from rdflib import Namespace, URIRef


class URIConstructor:
    """Namespaced URI constructor.

    The URIConstructor class is initialized given a namespace.
    Calls to the initialized object will construct rdflib.URIRefs for that namespace.

    If a hash_value argument of type str | bytes is provided, the URIRef
    will be generated with the sha256 hash of the hash_value argument as component;
    else a URIRef with a unique component will be generated using UUID4.
    """

    def __init__(
        self,
        namespace: str,
    ) -> None:
        self.namespace = Namespace(namespace)

    def __call__(self, hash_value: str | bytes | None = None) -> URIRef:
        if hash_value is None:
            segment = str(uuid4())
        else:
            if isinstance(hash_value, str):
                hash_value = hash_value.encode("utf8")

            digest = sha256(hash_value).hexdigest()
            segment = digest[:36]

        return self.namespace[segment]
