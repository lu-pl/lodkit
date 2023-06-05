from rdflib import Graph
from rdflib.compare import isomorphic

import lodkit.rdfimport
import rdftest_ttl, rdftest_xml

## this doesn't work yet..
## the importer doesn't search in submodules. Why?
# from graphs import rdftest_ttl, rdftest_xml


def test_ttl_import():
    """Check if import really is an rdflib.Graph."""
    assert isinstance(rdftest_ttl, Graph)


def test_xml_import():
    """Check if import really is an rdflib.Graph."""
    assert isinstance(rdftest_xml, Graph)


def test_iso_ttl_xml():
    """Check if imported graphs of different formats are isomorphic."""
    assert isomorphic(rdftest_ttl, rdftest_xml)
