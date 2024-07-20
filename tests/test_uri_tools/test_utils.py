"""Test for uri_tools.utils."""

from urllib.parse import quote, unquote
from hypothesis import given, strategies as st
from lodkit import mkuri_factory
from lodkit.uri_tools.utils import generate_uri_hash, generate_uri_id_segment

from rdflib import URIRef


@given(st.text())
def test_generate_uri_hash(text):
    """Check if URI hashes are URI save."""
    hashed: str = generate_uri_hash(text)
    assert quote(hashed) == unquote(hashed)


@given(st.text())
def test_generate_uri_id_segment_hash(text):
    """Check if hashed URI segments are URI save."""
    hashed_segment: str = generate_uri_id_segment(text)
    assert quote(hashed_segment) == unquote(hashed_segment)


@given(st.one_of(st.text(), st.none()))
def test_mkuri_factory(hash_value):
    """Check if hash-based URIs generated with a mkuri_factory are reproducable."""
    namespace: str = "https://test/namespace/"
    mkuri = mkuri_factory(namespace)
    uri = mkuri(hash_value=hash_value)

    # __repr__ test
    assert str(mkuri) == f"mkuri_factory(namespace='{namespace}')"
    assert isinstance(uri, URIRef)

    if hash_value is not None:
        uri2 = mkuri(hash_value)
        assert uri == uri2
