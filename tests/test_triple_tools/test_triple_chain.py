from lodkit import TripleChain, ttl
import pytest
from rdflib import Namespace
from rdflib.compare import isomorphic

ex = Namespace("https://example.com/")

t1 = ttl(ex.s, (ex.p, ex.o))
t2 = ttl(ex.s, (ex.p2, ex.o2))
t3 = ttl(ex.s, (ex.p3, ex.o3))


def generate_chain_params() -> list[TripleChain]:
    return [
        TripleChain(t1, t2, t3),
        TripleChain(t1, t2).chain(t3),
        TripleChain(t1).chain(t2, t3),
        TripleChain().chain(t1, t2, t3),
        #
        TripleChain().chain(t1, t2, t3).chain(),
        TripleChain().chain(t1, t2).chain(t3),
        TripleChain().chain(t1).chain(t2, t3),
        TripleChain().chain().chain(t1, t2, t3),
        #
        TripleChain(t1).chain(t2).chain(t3),
    ]


@pytest.mark.parametrize("chain", generate_chain_params())
def test_basic_triple_chain(chain):
    """Chain ttl objects and check if chains contain the same triples."""

    triples = ttl(ex.s, (ex.p, ex.o), (ex.p2, ex.o2), (ex.p3, ex.o3))
    assert list(chain) == list(triples)


@pytest.mark.parametrize("chain", generate_chain_params())
def test_basic_triple_chain_to_graph(chain):
    """Chain ttl objects and check if chains contain the same triples."""

    triples = ttl(ex.s, (ex.p, ex.o), (ex.p2, ex.o2), (ex.p3, ex.o3))
    assert isomorphic(triples.to_graph(), chain.to_graph())


@pytest.mark.parametrize("chain", generate_chain_params())
def test_basic_triple_chain_exhaustion(chain):
    """Check that a given chain is exausted after a call to to_graph."""

    assert chain.to_graph()
    assert not chain.to_graph()

    with pytest.raises(StopIteration):
        next(chain)

    msg = "Graph object '.+' is empty. This might indicate an exhausted iterator."
    with pytest.warns(UserWarning, match=msg):
        chain.to_graph()
