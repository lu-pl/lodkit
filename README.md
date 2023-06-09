![<img src="lodkit.png" width=50% height=50%>](./lodkit.png)

# LODKit
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

LODKit is a collection of Linked Open Data related Python functionalities. 

LODkit (includes|will include)
- a custom `rdflib.Graph` subclass that is capable of RDFS and OWL-RL inferencing 
- a custom importer for loading RDF files as if they where Python modules
- [...]

## Examples

### lodkit.Graph
`lodkit.Graph` is an `rdflib.Graph` subclass that is cabable of RFDS and OWL-RL inferencing.

The default plugin for inferencing is [owlrl](https://github.com/RDFLib/OWL-RL/)'s native Python inferencing engine. The deductive closure type used for `lodkit.Graph` is [RDFS_OWLRL_Semantics](https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html) which allows for RDFS *and* OWL-RL reasoning.

```python
from lodkit import Graph
from rdflib import Namespace

ex = Namespace("http://example.org/")

graph = Graph()
graph.add((ex.subj, ex.pred, ex.obj))
graph.add((ex.inverse, OWL.inverseOf, ex.pred))

print(len(graph))                # 2
# print(graph.serialize())

graph.inference(plugin="owlrl") 
print(len(graph))                # 359
# print(graph.serialize())
```

### lodkit.importer

`lodkit.importer` is a custom importer for importing RDF files as if they where regular Python modules.
RDF files are parsed into `rdflib.Graph` instances and made available in the module namespace.

E.g. in a directory structure

```text
├── dir/
│   ├── main.py
│   ├── some_rdf.ttl
│   ├── subdir/
│       └── some_more_rdf.xml
```

the following creates `rdflib.Graph` instances in the current module namespace:

```python
# main.py
import lodkit.importer

import some_rdf
from subdir import some_more_rdf

print(type(some_rdf))       # <class 'rdflib.graph.Graph'>
print(type(some_more_rdf))  # <class 'rdflib.graph.Graph'>
```
I find this really convenient for bulk-parsing graphs ([example](https://gitlab.com/lupl/rdfdf/-/blob/main/tests/test_corpus_table/test_corpus_table.py#L18)).

