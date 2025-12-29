"""Pytest entry point for basic lodkit.URIConstructor tests."""

from lodkit import URIConstructor


def test_uri_constructor_basic():
    make_uri = URIConstructor("https://example.com/")

    assert make_uri() != make_uri()
    assert make_uri("test") == make_uri("test")
