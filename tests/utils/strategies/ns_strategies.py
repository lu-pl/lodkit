"""Hypothesis strategies for lodkit.namespace_tools testing."""

from typing import Annotated
from typing import Annotated

from hypothesis import provisional as pr, strategies as st
from hypothesis.strategies._internal.strategies import SearchStrategy
from lodkit import tst_xml
from tests.utils.strategies.ttl_strategies import rdflib_namespaces


public_variable_names: Annotated[
    SearchStrategy, "Strategy for public Python variable names"
] = st.from_regex(r"^[a-z]+[a-z_]*$", fullmatch=True)

name_namespace_pairs: Annotated[
    SearchStrategy, "Strategy for variable_name/rdflib.Namespace tuples."
] = st.tuples(public_variable_names, rdflib_namespaces)

name_uri_pairs: Annotated[SearchStrategy, "Strategy for variable_name/URI tuples."] = (
    st.tuples(public_variable_names, pr.urls())
)

name_uriref_pairs: Annotated[
    SearchStrategy, "Strategy for variable_name/rdflib.URIRef tuples."
] = st.tuples(public_variable_names, tst_xml.triple_uris)


fail_pairs: Annotated[SearchStrategy, "Strategy for fail values."] = st.tuples(
    public_variable_names, st.one_of(st.integers(), st.none(), st.booleans())
)
