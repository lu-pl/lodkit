"""LODKit uriclass: A dataclass inspired URI constructor mechanism."""

from collections.abc import Iterable, Iterator
from types import new_class

from lodkit.uri_tools._types import _TURIConstructorFactory
from lodkit.uri_tools.utils import mkuri_factory


class uriclass:
    """Dataclass-inspired URI constructor.

    Class-level attributes are converted to URIs according to uri_constructor.
    For class attributes with just type information, URIs are constructed using UUIDs,
    for class attributes with string values, URIs are constructed using hashing based on that string.

    Examples:

        @uriclass(Namespace("https://test.org/test/"))
        class uris:
            x1: str

            y1 = "hash value 1"
            y2 = "hash value 1"

        print(uris.x1)             # Namespace("https://test.org/test/<UUID>")
        print(uris.y1 == uris.y2)  # True
    """

    def __init__(
        self,
        namespace: str,
        uri_constructor: _TURIConstructorFactory = mkuri_factory,
    ) -> None:
        self._mkuri = uri_constructor(namespace)

    def __call__[T](self, cls: T) -> T:
        # note: order matters, the second loop sets attributes in cls!
        for key, value in cls.__dict__.items():
            if not key.startswith("_"):
                setattr(cls, key, self._mkuri(value))

        for var, _ in cls.__annotations__.items():
            setattr(cls, var, self._mkuri())

        return cls


def make_uriclass(
    cls_name: str,
    namespace: str,
    fields: Iterable[str | tuple[str, str]],
    uri_constructor: _TURIConstructorFactory = mkuri_factory,
) -> type[uriclass]:
    """Constructor for dynamic URI class creation.

    make_uriclass provides functionality structurally equivalent to @uriclass,
    but fields are read from an Iterable[str | tuple[str, str]].

    Examples:

        uris = make_uriclass(
            cls_name="TestURIFun",
            namespace="https://test.org/test/",
            fields=("x", ("y1", "hash value 1"), ("y2", "hash value 1")),
        )

        print(uris.x1)             # Namespace("https://test.org/test/<UUID>")
        print(uris.y1 == uris.y2)  # True
    """
    _mkuri = uri_constructor(namespace)

    def _generate_pairs() -> Iterator[tuple[str, str]]:
        for field in fields:
            match field:
                case str():
                    yield (field, _mkuri())
                case (str(), str()):
                    name, value = field
                    yield (name, _mkuri(value))
                case _:
                    raise TypeError(
                        "Fields must be of type Iterable[str | tuple[str, str]]."
                    )

    _cls = new_class(
        name=cls_name, exec_body=lambda ns: ns.update(dict(_generate_pairs()))
    )
    return _cls
