"""Hypothesis strategies for LOD testing."""

from typing import Annotated, get_type_hints

from hypothesis import strategies as st
from hypothesis.strategies._internal.strategies import SearchStrategy
from rdflib import BNode, Literal, URIRef


# todo: Annotate with docs + lodkit.lod_types type; then st.register_type_strategy

triple_uri: SearchStrategy = st.builds(
    lambda x: URIRef(f"https://lodkit.testing_tools/{x}"), st.uuids()
)

triple_bnode: SearchStrategy = st.builds(lambda _: BNode(), st.integers())

triple_literal: SearchStrategy = st.builds(lambda x: Literal(x), st.text())

triple_subject: SearchStrategy = st.one_of(triple_uri, triple_bnode)

triple_predicate: SearchStrategy = triple_uri

triple_object: SearchStrategy = st.one_of(triple_uri, triple_bnode, triple_literal)

rdf_term: SearchStrategy = triple_object

triple: SearchStrategy = st.tuples(triple_subject, triple_predicate, triple_object)
