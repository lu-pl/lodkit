![<img src="lodkit.png" width=50% height=50%>](https://raw.githubusercontent.com/lu-pl/lodkit/main/lodkit.png)

# LODKit
![tests](https://github.com/lu-pl/lodkit/actions/workflows/tests.yaml/badge.svg)
[![coverage](https://coveralls.io/repos/github/lu-pl/lodkit/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/lu-pl/lodkit?branch=main&kill_cache=1)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://badge.fury.io/py/lodkit.svg)](https://badge.fury.io/py/lodkit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

<!-- <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> -->

LODKit is a collection of Linked Open Data related Python functionalities.


# Installation

# Usage

## RDF Importer

`lodkit.RDFImporter` is a custom importer for importing RDF files as if they were modules.

Assuming 'graphs/some_graph.ttl' exists in the import path, `lodkit.RDFImporter` makes it possible to do the following:
```python
import lodkit
from graphs import some_graph

type(some_graph)  # <class 'rdflib.graph.Graph'>
```

Note that `lodkit.RDFImporter` is available on `import lodkit`.

## Types
`lodkit.lod_types` defines several useful `typing.TypeAliases` and `typing.Literals` for working with RDFLib-based Python functionalities.

## URI Tools

### uriclass, make_uriclass

`uriclass` and `make_uriclass` provide dataclass-inspired URI constructor functionality.

With `uriclass`, class-level attributes are converted to URIs according to uri_constructor.
For class attributes with just type information, URIs are constructed using UUIDs,
for class attributes with string values, URIs are constructed using hashing based on that string.

```python
from lodkit import uriclass

@uriclass(Namespace("https://test.org/test/"))
class uris:
    x1: str

    y1 = "hash value 1"
    y2 = "hash value 1"

    print(uris.x1)             # Namespace("https://test.org/test/<UUID>")
    print(uris.y1 == uris.y2)  # True
```

`make_uriclass` provides equalent functionality but is more apt for dynamic use.

```python
from lodkit import make_uriclass

uris = make_uriclass(
    cls_name="TestURIFun",
	    namespace="https://test.org/test/",
        fields=("x", ("y1", "hash value 1"), ("y2", "hash value 1")),
    )

    print(uris.x1)             # Namespace("https://test.org/test/<UUID>")
    print(uris.y1 == uris.y2)  # True
```
	
### uritools.utils
`uritools.utils` defines base functionality for generating UUID-based and hashed URIs.

`URIConstructorFactory` (alias of `mkuri_factory`) constructs a callable for generating URIs.
The returned callable takes an optional str argument 'hash_value'; 
If a hash value is given, the segment is generated using a hash function, else the path is generated using a uuid.

```python
from lodkit import URIConstructorFactory

mkuri = URIConstructorFactory("https://test.namespace/")
print(mkuri())                         # URIRef("https://test.namespace/<UUID>")
print(mkuri("test") == mkuri("test"))  # True
```

## Triple Tools
Triple tools (so far only) defines `lodkit.ttl`, a triple constructor implementing a Turtle-like interface.

`lodkit.ttl` aims to implement [turtle predicate list notation](https://www.w3.org/TR/turtle/#predicate-lists) by taking a triple subject and predicate-object pairs;
objects in a predicate-object pair can be 

- objects of type `lodkit._TripleObject` (strings are also permissible and are interpreted as `rdflib.Literal`),
- tuples of `lodkit._TripleObject` (see [turtle object lists](https://www.w3.org/TR/turtle/#object-lists)),
- lists of predicate-object pairs, emulating [turtle blank node notation](https://www.w3.org/TR/turtle/#BNodes).
- `lodkit.ttl` objects.

```python
from collections.abc import Iterator

from lodkit import _Triple, ttl
from rdflib import Graph, Literal, RDF, RDFS, URIRef


triples: Iterator[_Triple] = ttl(
    URIRef("https://subject"),
    (RDF.type, URIRef("https://some_type")),
    (RDFS.label, (Literal("label 1"), "label 2")),
    (RDFS.seeAlso, [(RDFS.label, "label 3")]),
    (
        RDFS.isDefinedBy,
        ttl(URIRef("https://subject_2"), (RDF.type, URIRef("https://another_type"))),
    ),
)

graph: Graph = triples.to_graph()
```

The above graph serialized to turtle:
```ttl
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://subject> a <https://some_type> ;
    rdfs:label "label 1",
        "label 2" ;
    rdfs:isDefinedBy <https://subject_2> ;
    rdfs:seeAlso [ rdfs:label "label 3" ] .

<https://subject_2> a <https://another_type> .
```

## Namespace Tools

### NamespaceGraph
`lodkit.NamespaceGraph` is a simple rdflib.Graph subclass for easy and convenient namespace binding.

```python
from lodkit import NamespaceGraph
from rdflib import Namespace

class CLSGraph(NamespaceGraph):
	crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
	crmcls = Namespace("https://clscor.io/ontologies/CRMcls/")
	clscore = Namespace("https://clscor.io/entity/")

graph = CLSGraph()

ns_check: bool = all(
	ns in map(lambda x: x[0], graph.namespaces())
	for ns in ("crm", "crmcls", "clscore")
)

print(ns_check)  # True
```

## ClosedOntologyNamespace, DefinedOntologyNamespace
`lodkit.ClosedOntologyNamespace` and `lodkit.DefinedOntologyNamespace` are `rdflib.ClosedNamespace` and `rdflib.DefinedNameSpace` subclasses 
that are able to load namespace members based on an ontology.

```python
crm = ClosedOntologyNamespace(ontology="./CIDOC_CRM_v7.1.3.ttl")

crm.E39_Actor   # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Actor')
crm.E39_Author  # AttributeError
```

```python
class crm(DefinedOntologyNamespace):
	ontology = "./CIDOC_CRM_v7.1.3.ttl"

crm.E39_Actor   # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Actor')
crm.E39_Author  # URIRef('http://www.cidoc-crm.org/cidoc-crm/E39_Author') + UserWarning
```


Note that `rdflib.ClosedNamespaces` are meant to be instantiated and `rdflib.DefinedNameSpaces` are meant to be extended,
which is reflected in `lodkit.ClosedOntologyNamespace` and `lodkit.DefinedOntologyNamespace`.


## Testing Tools
`lodkit.testing_tools` aims to provide general definitions (e.g Graph format options) and [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) strategies useful for testing RDFLib-based Python and code.

E.g. the `TripleStrategies.triples` strategy generates random triples utilizing all permissible subject, predicate and object types including lang-tagged and xsd-typed literals.
The following uses the triples strategies together with a Hypothesis strategy to create random graphs:

```python
from hypothesis import given, strategies as st
from lodkit import tst
from rdflib import Graph


@given(triples=st.lists(tst.triples, min_size=1, max_size=10))
def test_some_function(triples):
    graph = Graph()
    for triple in triples:
        graph.add(triple)

    assert len(graph) == len(triples)
```

The strategy generates up to 100 (by default, see [settings](https://hypothesis.readthedocs.io/en/latest/settings.html)) lists of 1-10 `tuple[_TripleSubject, URIRef, _TripleObject]` and passes them to the test function.

> Warning: The API of lodkit.tesing_tools is very likely to change soon! Strategies should be module-level callables and not properties of a Singleton.
