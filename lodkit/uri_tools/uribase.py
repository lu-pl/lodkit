"""Experimental URI constructor mechanism."""

import re

from lodkit.uri_tools.utils import mkuri_factory
from rdflib import Namespace, URIRef


class InstantiationException(Exception):
    """Exception for indicating that instantiating a class is not permitted."""


def _URIConstructorMetaFactory(namespace: str) -> type:
    """Factory for creating a URINamespace Metaclass."""
    _namespace = Namespace(namespace)
    mkuri = mkuri_factory(_namespace)

    class AutoDict(dict):
        """Dict subclass that generates a URI for missing keys.

        This is intended to be used in the __prepare__ namespace hook
        for resolving missing attributes with a URI constructor.
        """

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(self, *args, **kwargs)

        def __missing__(self, key) -> URIRef:
            self[key] = uri = mkuri()
            return uri

    class MetaURIConstructor(type):
        """URINamespace Metaclass.

        Resolves class attributes with a URI constructor.
        The behavior is inspired by dataclasses and the like.

        Note: Class attributes with values are handled by __new__,
        'loose' class attributes (which would normally cause a NameError)
        are caught by the __prepare__ hook and deligated to AutoDict.
        """

        def __new__(mcls, name, bases, cls_dict):
            """Meta constructor for converting public class attributes of a mesaclass into URIs."""
            for key, value in cls_dict.items():
                if (re.match(r"^__.+__$", key) is None) and isinstance(value, str):
                    cls_dict.update({key: mkuri(value)})

            return super().__new__(mcls, name, bases, cls_dict)

        @classmethod
        def __prepare__(mcls, name, bases, **kwargs) -> dict:
            return AutoDict()

    return MetaURIConstructor


def uribase(namespace: str) -> type:
    """Base class factory for a URI constructor.

    Returns a URIConstructor base class with a pre-loaded metaclass.
    For subclasses of that base class, class-level attributes are converted to URIs.

    For 'loose' class attributes, URIs are constructed using UUIDs,
    for class attributes with string values, URIs are constructed using hashing based on that string.

    Note that this is experimental, probably not a good idea
    and that linters will (rightfully!) flag 'loose' class attributes.

    Example:
    class namespace(uribase("https://some.namespace/test/)):
        x, y, z
        another_uri="hash value"

    namespace.x            #  https://some.namespace/test/<uuid>
    namespace.another_uri  #  https://some.namespace/test/<hash 'hash value'>)
    """

    class URIConstructor(metaclass=_URIConstructorMetaFactory(namespace)):
        def __init__(self):
            raise InstantiationException(
                f"'{type(self).__name__}' must not be instantiated."
            )

    return URIConstructor
