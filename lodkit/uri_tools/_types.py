"""Type definitions for lodkit.uri_tools."""

from typing import Any, Protocol


class _TSegmentCallBack(Protocol):
    """Minimal callback protocol for segment_callbacks (e.g. generate_uri_id_segment).

    See https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols.
    """

    def __call__(
        self, hash_value: str | None = None, *args: Any, **kwargs: Any
    ) -> str: ...


class _TURIConstructor(Protocol):
    """Minimal callback protocol for URIConstructor."""

    def __call__(self, hash_value: str | None = None) -> str: ...


class _TURIConstructorFactory(Protocol):
    """Minimal callback protocol for URIConstructorFactory."""

    def __call__(
        self,
        namespace: str,
        *args: Any,
        **kwargs: Any,
    ) -> _TURIConstructor: ...
