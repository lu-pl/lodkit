"""Functionality for constructing URIs."""

from collections.abc import Callable
import hashlib
from typing import Annotated
from uuid import uuid4

from lodkit.uri_tools._types import _TSegmentCallBack, _TURIConstructor
from rdflib import Namespace


def generate_uri_hash(
    hash_value: str, length: int | None = 10, hash_function: Callable = hashlib.sha256
) -> str:
    """Generate a truncated URL-safe string hash.

    Pass length=None for an untruncated hash.
    """
    _hash = hash_function(hash_value.encode("utf-8")).hexdigest()
    return _hash[:length]


def generate_uri_id_segment(
    hash_value: str | None = None,
    length: int | None = 10,
    hash_function: Callable = hashlib.sha256,
    uuid_function: Callable = uuid4,
) -> str:
    """Generate a URI ID segment.

    URI ID segment here means either the fragment or the last path segment of a URI.

    If a hash value is given, the segment is generated using
    a hash function, else the path is generated using a uuid.
    """
    _segment: str = (
        str(uuid_function())
        if hash_value is None
        else generate_uri_hash(hash_value, length=length, hash_function=hash_function)
    )
    return _segment


def mkuri_factory(
    namespace: str,
    generate_segment_id_callback: _TSegmentCallBack = generate_uri_id_segment,
) -> _TURIConstructor:
    """Factory for generating URI constructor callables.

    The returned callable takes an optional str argument 'hash_value';
    If a hash value is given, the segment is generated using a hash function, else the path is generated using a uuid.
    """

    class _mkuri:
        def __repr__(self) -> str:
            return f"mkuri_factory(namespace='{namespace}')"

        def __call__(self, hash_value: str | None = None) -> str:
            return Namespace(namespace)[
                generate_segment_id_callback(hash_value=hash_value)
            ]

    return _mkuri()


URIConstructorFactory: Annotated[
    Callable, "Alias for 'mkuri_factory'. Possible future deprecation."
] = mkuri_factory
