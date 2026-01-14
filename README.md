<img src="lodkit.svg" width="50%" height="50%" />

![tests](https://github.com/lu-pl/lodkit/actions/workflows/tests.yaml/badge.svg)
[![coverage](https://coveralls.io/repos/github/lu-pl/lodkit/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/lu-pl/lodkit?branch=main&kill_cache=1)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![PyPI version](https://badge.fury.io/py/lodkit.svg)](https://badge.fury.io/py/lodkit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

<!-- <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> -->

LODKit is a collection of Linked Open Data related Python functionalities.


# Installation

LODKit is available on PyPI:

```shell
pip install lodkit
```

# Usage

## Triple Constructor

The `lodkit.ttl` triple constructor implements a Turtle-inspired functional DSL for RDF Graph generation.

`lodkit.ttl` aims to emulate RDF Turtle syntax by featuring Python equivalents for

- [Predicate List notation](https://www.w3.org/TR/turtle/#predicate-lists)
- [Object List notation](https://www.w3.org/TR/turtle/#object-lists)
- [Blank Node notation](https://www.w3.org/TR/turtle/#BNodes)
- [RDF Collections](https://www.w3.org/TR/turtle/#collections)

and is recursive/composable on all code paths.

`lodkit.ttl` implements the `Iterable[lodkit.types.Triple]` protocol and exposes a `to_graph` method for convenient construction of an `rdflib.Graph` instance.

### Examples

The following examples show features of the `lodkit.ttl` triple constructor and display the equivalent RDF graph for comparison.

#### Predicate List notation

The `lodkit.ttl` constructor takes a triple subject and an arbitrary number of triple predicate-object constellations as input; this aims to emulate Turtle Predicate List notation.

The constructor accepts any RDFLib-compliant triple object in the object position, plain strings are interpreted as `rdflib.Literal`.

```python
from lodkit import ttl
from rdflib import Namespace

ex = Namespace("https://example.com/")

triples = ttl(
    ex.s,
    (ex.p, ex.o),
    (ex.p2, "literal")
)
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p ex:o ;
    ex:p2 "literal" .
```

#### Object List notation

Predicate-object constellation arguments in `lodkit.ttl` can be of arbitrary length; the first element is interpreted as triple predicate, all succeeding elements are interpreted as Turtle Object List.

```python
triples = ttl(
    ex.s,
    (ex.p, ex.o1, ex.o2, "literal")
)
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p ex:o1, ex:o2, "literal" .
```

#### Blank Node notation

Python lists (of predicate-object constellations) in the object position of predicate-object constellations are interpreted as Turtle Blank Nodes.

```python
triples = ttl(
    ex.s,
    (
        ex.p, [
            (ex.p2, ex.o),
            (ex.p3, "1", "2")
        ]
    )
)
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p [ 
	ex:p2 ex:o ;
	ex:p3 "1", "2" 
] .
```

#### RDF Collections
Python tuples in the object position of predicate-object constellations are interpreted as Turtle Collection:

```python
triples = ttl(
    ex.s,
    (ex.p, (ex.o, "1", "2", "3"))
)
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p ( ex:o "1" "2" "3" ) .
```

#### Recursion on all paths

One of the strengths of `lodkit.ttl` is that it is recursive on all code paths.

To demonstrate the composability of the `lodkit.ttl` constructor, one could e.g. define a `lodkit.ttl` object that has another `lodkit.ttl` object and a blank node with an object list and yet another `lodkit.ttl` object (in a single element RDF Collection) defined within an RDF Collection:


```python
triples = ttl(
    ex.s,
    (
        ex.p,
        (
            ttl(ex.s2, (ex.p2, "1")),
            [
                (ex.p3, "2", "3"),
                (ex.p4, (ttl(ex.s3, (ex.p5, "4")),))
            ],
        ),
    ),
)
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p ( 
	ex:s2 
	[ 
		ex:p3 "2", "3" ;
        ex:p4 ( ex:s3 ) 
	] 
) .

ex:s2 ex:p2 "1" .

ex:s3 ex:p5 "4" .
```

This is actually a relatively simple example. Triple objects in the `lodkit.ttl` constructor can be *arbitrarily* nested. 

`lodkit.ttl` is pretty recursive! :)


### Building Triple Chains

As mentioned, `lodkit.ttl` implements the `Iterable[lodkit.types.Triple]` protocol; arbitrary `lodkit.ttl` instances can therefore be chained to create highly modular and scalable triple generation pipelines.

A minimal example of such a (layered) triple pipeline could look like this:

```python
class TripleGenerator:

    def triple_generator_1(self) -> Iterator[Triple]:
        if conditional:
            yield (s, p, o)
        yield from ttl(s, ...)

    # more triple generator method definitions
    ...

    def __iter__(self) -> Iterator[Triple]:
        return itertools.chain(
            self.triple_generator_1(),
            self.triple_generator_2(),
            self.triple_generator_3(),
            ...
        )

triples: Iterator[Triple] = itertools.chain(TripleGenerator(), ...)
```

## TripleChain

LODKit provides a `TripleChain` class for convenient triple chain construction. Also see [Building Triple Chains](#building-triple-chains).

`lodkit.TripeChain` is a simple `itertools.chain` subclass that implements a fluid chain interface for arbitrary successive chaining and a `to_graph` method for deriving an `rdflib.Graph` from a given chain.

> Note that, unlike `lodkit.ttl`, `TripleChain` is an `Iterator` and can be exhausted, e.g. by calling `TripleChain.to_graph`.

```python
from collections.abc import Iterator

from lodkit import TripleChain, ttl
from lodkit.types import Triple
from rdflib import Graph, Namespace

ex = Namespace("https://example.com/")


triples = ttl(ex.s, (ex.p, "1", "2", "3"))
more_triples = ttl(ex.s, (ex.p2, [(ex.p3, ex.o)]))
yet_more_triples = ttl(ex.s, (ex.p3, ex.o))


def any_iterable_of_triples() -> Iterator[Triple]:
    yield (ex.s, ex.p, ex.o)


triple_chain = (
    TripleChain(triples, more_triples)
    .chain(yet_more_triples)
    .chain(any_iterable_of_triples())
)

ex_graph = Graph()
ex_graph.bind("ex", ex)

graph: Graph = triple_chain.to_graph(graph=ex_graph)
print(graph.serialize())
```

```ttl
@prefix ex: <https://example.com/> .

ex:s ex:p ex:o,
        "1",
        "2",
        "3" ;
    ex:p2 [ ex:p3 ex:o ] ;
    ex:p3 ex:o .
```


## RDF Importer

`lodkit.RDFImporter` is a custom importer for parsing RDF files into `rdflib.Graph` objects.

Assuming `graphs/some_graph.ttl` exists in the import path, `lodkit.RDFImporter` makes it possible to import the RDF file like a module:

```python
from graphs import some_graph

type(some_graph)  # <class 'rdflib.graph.Graph'>
```

RDF import functionality is available after registering `lodkit.RDFImporter` with the import maschinery e.g by calling `lodkit.enable_rdf_import`.

## Types

`lodkit.types` defines several useful types for working with RDFLib-based Python code.

## URI Tools

### URIConstructor

The `URIConstructor` class provides namespaced URI constructor functionality.

A `URIConstructor` is initialized given a namespace.
Calls to the initialized object will construct `rdflib.URIRefs` for that namespace.

If a `hash_value` argument of type `str | bytes` is provided, the URIRef will be generated with the sha256 hash of the `hash_value` argument as last URI component;
else a URIRef with a unique component will be generated using UUID4.

```python
make_uri = URIConstructor("https://example.com/")

make_uri()        # rdflib.URIRef('https://example.com/<UUID4>')
make_uri("test")  # rdflib.URIRef('https://example.com/<sha256>')

make_uri("test") == make_uri("test")  # True
```

## Namespace Tools

### ClosedOntologyNamespace

`ClosedOntologyNamespace` is an `rdflib.namespace.ClosedNamespace`-inspired utility class that constructs an immutable (*closed*) mapping of RDF term names to IRIs based on an Ontology or generally an RDF graph source.

Given a `lodkit.types.GraphParseSource` or an `rdflib.Graph`, a `MappingProxyType[str, rdflib.URIRef]` mapping is created and stored in `ClosedOntologyNamespace.mapping` by 

1. Querying the RDF source for RDF class and property definitions (RDF/RDFS/OWL class/property type assertions and OWL named individual assertions)

2. Deriving RDF term names by extracting the last IRI component delimited by `#`, `/` or `:` for generating the RDF term name -> IRI mapping.


Namespace members are accessible as both attributes and items of a given `ClosedOntologyNamespace` instance, i.e. attribute and item access is routed to `ClosedOntologyNamespace.mapping`.
For dictionary operations over the namespace mapping, the public `ClosedOntologyNamespace.mapping` can be accessed directly.


The following example loads a remote Ontology and accesses namespace members using attribute and item lookup.

```python
from lodkit import ClosedOntologyNamespace

crm = ClosedOntologyNamespace(
    source="https://cidoc-crm.org/rdfs/7.1.3/CIDOC_CRM_v7.1.3.rdf"
)

crm.E92_Spacetime_Volume  # URIRef('http://www.cidoc-crm.org/cidoc-crm/E92_Spacetime_Volume')
crm["E52_Time-Span"]      # URIRef('http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span')

crm.E21_Author            # AttributeError
crm["E21-Person"]         # AttributeError
```

> Note that lookup failure for both attribute and item access on `ClosedOntologyNamespace` objects raises an `AttributeError`!

In the case of RDF term names conflicting with class namespace names, the class namespace names take precedence for attribute access; conflicting RDF terms are still accessible via item lookup or through the `ClosedOntologyNamespace.mapping` proxy.

> Note that *currently* `ClosedOntologyNamespace` is a highly dynamic runtime construct and does not support static analysis and IDE completion for namespace entries.
	
	
