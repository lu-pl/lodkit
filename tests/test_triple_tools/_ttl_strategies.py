"""Hypothesis strategies for ttl testing."""

from functools import partial
from typing import Annotated

from hypothesis import given, provisional as pr, settings, strategies as st
from hypothesis.strategies._internal.strategies import SearchStrategy
from lodkit import ttl
from lodkit.testing_tools.strategies import (
    triple_bnode,
    triple_literal,
    triple_object,
    triple_predicate,
)
from rdflib import BNode, Namespace, URIRef


ttl_object: Annotated[SearchStrategy, "Strategy for ttl object values."] = st.one_of(
    triple_object, st.text()
)

predicate_object_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-object pairs."
] = st.tuples(triple_predicate, ttl_object)

predicate_pair_pairs: Annotated[SearchStrategy, "Strategy for ttl bnode objects."] = (
    st.tuples(triple_predicate, st.lists(predicate_object_pairs))
)

predicate_list: Annotated[SearchStrategy, "Strategy for ttl predicate lists."] = (
    st.lists(triple_object, min_size=1).map(tuple)
)

ttl_instances: Annotated[SearchStrategy, "Strategy for ttl instances."] = st.builds(
    partial(ttl, URIRef("https://lodkit.testing_tools/static_subject")),
    predicate_object_pairs,
)

predicate_ttl_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-ttl pairs."
] = st.tuples(triple_predicate, ttl_instances)

predicate_iterator_pairs: Annotated[
    SearchStrategy, "Strategy for ttl predicate-iterator pairs."
] = st.tuples(triple_predicate, st.iterables(predicate_object_pairs, max_size=5))

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
        triple_bnode,
        triple_literal,
    ),
    triple_object,
)

fail_object_pairs: Annotated[
    SearchStrategy, "Strategy for _TripleObject typecheck fails."
] = st.tuples(
    triple_predicate,
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
