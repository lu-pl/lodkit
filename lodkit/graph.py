"""rdflib.Graph subclasses with plugin-based inferencing capability."""

import inspect
import sys

from typing import Optional, Literal, Generator
from types import ModuleType

import rdflib

from lodkit import reasoners


_Reasoner = reasoners.Reasoner
_ReasonerLiterals = Literal[*reasoners.reasoners.keys()]
_ReasonerReference = _Reasoner | _ReasonerLiterals


class Graph(rdflib.Graph):
    """Subclass of rdflib.Graph with inferencing capability."""

    _default_reasoner = "owlrl"

    def __init__(self,
                 reasoner: Optional[_ReasonerReference] = None,
                 *args, **kwargs) -> None:
        """Initialize a lodkit.Graph."""
        self.reasoner = reasoner or self._default_reasoner
        super().__init__(*args, **kwargs)

    def _resolve_reasoner(self,
                          reasoner: _ReasonerReference) -> _Reasoner:
        """Get an actual _Reasoner instance from a _ReasonerReference."""
        match reasoner:
            case str():
                return reasoners.reasoners[reasoner]
            case _Reasoner():
                return reasoner
            case _:
                raise Exception("Reasoner not seizable.")

    def inference(self,
                  reasoner: Optional[_ReasonerReference] = None) -> rdflib.Graph:
        """Perform inferencing according to an InferencePlugin."""
        # get an actual Reasoner
        _reasoner_reference: _ReasonerReference = reasoner or self._default_reasoner
        _reasoner: _Reasoner = self._resolve_reasoner(_reasoner_reference)

        # call the reasoner
        return _reasoner.inference(self)


def get_subclasses(klass: type,
                   module: Optional[ModuleType] = None
                   ) -> Generator:
    """Get all subclasses of a type klass in a module.

    Default for the module parameter is the module of the type klass.
    """
    if module is None:
        module = sys.modules[klass.__module__]

    yield from filter(
        lambda cls: (
            inspect.isclass(cls) and
            issubclass(cls, klass) and
            klass in cls.__mro__ and
            cls is not klass
        ),
        (cls for cls_name, cls in inspect.getmembers(module))
    )


def get_direct_subclasses(klass: type,
                          module: Optional[ModuleType] = None
                          ) -> Generator:
    """Get /direct/ subclasses of a type klass in a module.

    Default for the module parameter is the module of the type klass.
    """
    yield from filter(
        lambda cls: klass in cls.__bases__,
        get_subclasses(klass, module)
    )


def subclass_bases_mapping() -> Generator[tuple[str, tuple], None, None]:
    """Replace rdflib.Graph with lodkit.Graph in rdflib.Graph subclasses."""
    for subclass in get_subclasses(rdflib.Graph):
        # for direct subclasses swap rdflib.Graph with lodkit.Graph in bases
        if subclass in get_direct_subclasses(rdflib.Graph):
            bases = list(subclass.__bases__)
            bases[bases.index(rdflib.Graph)] = Graph
            subclass.__bases__ = tuple(bases)

        yield (subclass.__name__, subclass)


# add subclasses to the current module namespace (i.e. import them)
_current_module_namespace = sys.modules[__name__].__dict__
_current_module_namespace.update(subclass_bases_mapping())
