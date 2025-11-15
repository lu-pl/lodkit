"""Hypothesis strategies for ttl testing."""

from functools import partial
from typing import Annotated

from hypothesis import provisional as pr, strategies as st
from hypothesis.strategies._internal.strategies import SearchStrategy
from lodkit import tst_xml, ttl
from rdflib import Namespace, URIRef


untyped_predicate_object_pairs: Annotated[
    SearchStrategy,
    """Strategy for predicate-object pairs without typed literals.
    XSD-type information gets lost for some reason when serializing graphs and re-parsing graphs.
    This is a kludge to remedy this, but the whole problem needs resolving.
    """,
] = st.tuples(
    tst_xml.triple_predicates,
    st.one_of(
        tst_xml.triple_uris,
        tst_xml.triple_bnodes,
        st.one_of(tst_xml.triple_literals_plain, tst_xml.triple_literals_lang_tagged),
    ),
)

predicate_object_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-object pairs."
] = st.tuples(tst_xml.triple_predicates, tst_xml.triple_objects)

predicate_pair_pairs: Annotated[SearchStrategy, "Strategy for ttl bnode objects."] = (
    st.tuples(tst_xml.triple_predicates, st.lists(predicate_object_pairs))
)

predicate_list: Annotated[SearchStrategy, "Strategy for ttl predicate lists."] = (
    st.lists(tst_xml.triple_objects, min_size=1).map(tuple)
)

ttl_instances: Annotated[SearchStrategy, "Strategy for ttl instances."] = st.builds(
    partial(ttl, URIRef("https://lodkit.testing_tools/static_subject")),
    predicate_object_pairs,
)

predicate_ttl_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-ttl pairs."
] = st.tuples(tst_xml.triple_predicates, ttl_instances)

predicate_iterator_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-iterator pairs."
] = st.tuples(
    tst_xml.triple_predicates, st.iterables(predicate_object_pairs, max_size=5)
)

rdflib_namespaces: Annotated[SearchStrategy, "Strategy for rdflib.Namespaces"] = (
    st.builds(Namespace, pr.urls())
)

fail_uris: Annotated[SearchStrategy, "Strategy for URIRef typecheck fails."] = (
    st.one_of(st.text(), rdflib_namespaces)
)

fail_predicate_pairs: Annotated[
    SearchStrategy, "Strategy for _TriplePredicate typecheck fails."
] = st.tuples(
    st.one_of(
        st.text(),
        rdflib_namespaces,
        tst_xml.triple_bnodes,
        tst_xml.triple_literals,
    ),
    tst_xml.triple_objects,
)

fail_object_pairs: Annotated[
    SearchStrategy, "Strategy for _TripleObject typecheck fails."
] = st.tuples(
    tst_xml.triple_predicates,
    st.one_of(
        st.integers(),
        st.floats(),
        st.functions(),
        st.sets(st.integers()),
        st.frozensets(st.integers()),
        st.none(),
        st.nothing(),
    ),
)
