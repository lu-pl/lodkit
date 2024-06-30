"""Tests for LOD-related Hypothesis strategies."""

from io import StringIO
from xml.sax import make_parser

from typeguard import check_type

from hypothesis import given, strategies as st
from lodkit import (
    _Triple,
    _TripleObject,
    _TriplePredicate,
    _TripleSubject,
    tst,
    tst_xml,
)
from rdflib import BNode, Literal, URIRef


@given(tst_xml.xml_parsable_text)
def test_parse_xml_parsable_text(xml_parsable_text):
    """Check if xml_parsable_text sampels are indeed xml-parsable."""
    parser = make_parser()
    to_parse = StringIO(rf"<element>{xml_parsable_text}</element>")
    parser.parse(to_parse)


@given(tst.triple_uris, tst_xml.triple_uris)
def test_typecheck_triple_uris(uri, uri_xml):
    """Typecheck triple_uris strategy."""
    check_type(uri, URIRef)
    check_type(uri_xml, URIRef)


@given(tst.triple_predicates, tst_xml.triple_predicates)
def test_typecheck_triple_predicates(predicate, predicate_xml):
    """Typecheck triple_predicates strategy."""
    check_type(predicate, _TriplePredicate)
    check_type(predicate_xml, _TriplePredicate)


@given(tst.triple_bnodes, tst_xml.triple_bnodes)
def test_typecheck_triple_bnodes(bnode, bnode_xml):
    """Typecheck triple_bnodes strategy."""
    check_type(bnode, BNode)
    check_type(bnode_xml, BNode)


@given(tst.triple_literals, tst_xml.triple_literals)
def test_typecheck_all_literals(literal, literal_xml):
    """Typecheck all literal strategies."""
    check_type(literal, Literal)
    check_type(literal_xml, Literal)


@given(tst.triple_literals_lang_tagged, tst_xml.triple_literals_lang_tagged)
def test_triple_literals_lang_tagged(literal, literal_xml):
    """Check if lang-tagged literals are indeed lang-tagged."""
    check_type(literal, Literal)
    check_type(literal_xml, Literal)

    assert literal.language is not None
    assert literal_xml.language is not None


@given(tst.triple_subjects, tst_xml.triple_subjects)
def test_typecheck_triple_subjects(subject, subject_xml):
    """Typecheck triple_subjects strategy."""
    check_type(subject, _TripleSubject)
    check_type(subject_xml, _TripleSubject)


@given(tst.triple_objects, tst_xml.triple_objects)
def test_typecheck_triple_objects(objects, objects_xml):
    """Typecheck triple_subjects strategy."""
    check_type(objects, _TripleObject)
    check_type(objects_xml, _TripleObject)


@given(tst.triples, tst_xml.triples)
def test_typecheck_triple(triple, triple_xml):
    """Typecheck triples strategy."""
    check_type(triple, _Triple)
    check_type(triple_xml, _Triple)


@given(tst.triple_literals_xsd_typed, tst_xml.triple_literals_xsd_typed)
def test_literals_xsd_typeds(literal, literal_xml):
    """Check if xsd-typed literals are indeed xsd-typed."""
    check_type(literal, Literal)
    check_type(literal_xml, Literal)

    assert literal.datatype is not None
    assert literal_xml.datatype is not None
