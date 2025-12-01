from collections.abc import Iterable
import itertools
from typing import Self

from lodkit import _Triple
from lodkit.triple_tools.utils import _ToGraphMixin


class TripleChain(itertools.chain[_Triple], _ToGraphMixin):
    """A simple itertools.chain for chaining lodkit._Triple iterables.

    TripleChain implements a fluid chain interface,
    i.e TripleChain objects can be chained repeatedly.

    TripleChain also exposes a to_graph method that generates a Graph
    from the triples stored in the TripleChain.
    Note that calling to_graph exhausts the TripleChain object.
    """

    def chain(self, *others: Iterable[_Triple]) -> Self:
        return self.__class__(self, *others)
