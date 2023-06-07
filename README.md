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
[...]

### lodkit.importer

`lodkit.importer` is a custom importer for importing RDF files as if they where regular Python modules.
RDF files are parsed into `rdflib.Graph` instances and made available in the module namespace.

E.g. in a directory structure

```text
├── dir/
│   ├── main.py
│   ├── some_rdf.ttl
│   ├── subdir/
│   │   └── some_more_rdf.xml
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


