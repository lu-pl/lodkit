# Changelog

## [0.7.0](https://github.com/lu-pl/lodkit/compare/v0.6.0...v0.7.0) (2026-10-19)


### ⚠ BREAKING CHANGES

* **ttl:** raise ValueError instead of TypeError
* **types:** remove T-prefixes from `lodkit.ttl` type names

### Features

* add `literal` rdflib.Literal constructor ([5afd04f](https://github.com/lu-pl/lodkit/commit/5afd04f4325ece9acf5996a77e956afdeb037078))
* add support for `[]` in subject position in the ttl constructor ([7c32566](https://github.com/lu-pl/lodkit/commit/7c325667697fac486505c73b19d8211f7b2fb20a))
* add support for rdfs:Datatype to ClosedOntologyNamespace ([5354ad8](https://github.com/lu-pl/lodkit/commit/5354ad851a67a150123daaedcb057c5d7a063019))
* **ttl:** add support for Python object literals ([51ff6a1](https://github.com/lu-pl/lodkit/commit/51ff6a128102d6218ce3b951ba86d44ba8327bde))
* **types:** add `TypedLiteral` type and sync with `LiteralToPython` ([53584cf](https://github.com/lu-pl/lodkit/commit/53584cf576d415f2e73a532805d7d9b92395fa0e))


### Bug Fixes

* remove sha256 truncation in lodkit.URIConstructor ([97758dd](https://github.com/lu-pl/lodkit/commit/97758dd18225077a2f7174467c06632d12a4a7e2))
* **ttl:** guard against single-element `PredicateObjectpair` ([06e484e](https://github.com/lu-pl/lodkit/commit/06e484e086fdb516890b83580e850eb3562dc172))
* **ttl:** handle empty RDF lists correctly in `lodkit.ttl` ([c7301de](https://github.com/lu-pl/lodkit/commit/c7301de7caaa593030515279e723b1d674f3a48e))
* **ttl:** raise ValueError instead of TypeError ([a865b7b](https://github.com/lu-pl/lodkit/commit/a865b7bbe2172c2af0bcba42b420f5f583b0f0b7))


### Documentation

* add docs section for `lodkit.literal` constructor ([b0739f1](https://github.com/lu-pl/lodkit/commit/b0739f1bdded5ec1c770b27b7f8a99a010581f48))
* cleanup README ([b5fd597](https://github.com/lu-pl/lodkit/commit/b5fd59765a4e3ff156ae935302604fe1fb9420d8))
* **readme:** add BNode subject factory section ([4dd8943](https://github.com/lu-pl/lodkit/commit/4dd89432ca0463bf84250d8392836e3f04af46c6))


### Code Refactoring

* **types:** remove T-prefixes from `lodkit.ttl` type names ([b468ec9](https://github.com/lu-pl/lodkit/commit/b468ec9d607395569d737b5599e01eec048b9ade))

## [0.6.0](https://github.com/lu-pl/lodkit/compare/v0.5.0...v0.6.0) (2026-01-15)


### ⚠ BREAKING CHANGES

* discontinue old namespace_tools functionality

### Features

* add GraphParseSource type ([6c6bf9f](https://github.com/lu-pl/lodkit/commit/6c6bf9f43885dc1495d9b6adb66563188108d5e4))
* implement ClosedOntologyNamespace ([0c05102](https://github.com/lu-pl/lodkit/commit/0c0510222b804d965aa1a8fc4abe0c0a0a169fd1))


### Documentation

* add README section on ClosedOntologyNamespace ([c08e673](https://github.com/lu-pl/lodkit/commit/c08e673d2e76fc95c2cac0afe6bb028443e0f242))


### Miscellaneous Chores

* discontinue old namespace_tools functionality ([5f736ca](https://github.com/lu-pl/lodkit/commit/5f736cac031a2a125d5add1a33c0965ef630ea44))

## [0.5.0](https://github.com/lu-pl/lodkit/compare/v0.4.0...v0.5.0) (2025-12-29)


### ⚠ BREAKING CHANGES

* implement simplified URIConstructor
* discontinue uriclass, make_uriclass and uribase
* define __all__ for types module and remove from top-level API
* rename type definitions
* re-implement RDFImporter

### Features

* add LiteralToPython type definition ([3e14d39](https://github.com/lu-pl/lodkit/commit/3e14d395bb73a322ee2fc2c81b0930997fa8e6b6))
* define __all__ for types module and remove from top-level API ([25c06c5](https://github.com/lu-pl/lodkit/commit/25c06c5f90adb76af8331a4e32227a4dc1fab934))
* discontinue uriclass, make_uriclass and uribase ([746b167](https://github.com/lu-pl/lodkit/commit/746b167528fd2e07911e5d801abc79bd3e7fb840))
* implement simplified URIConstructor ([f7973bd](https://github.com/lu-pl/lodkit/commit/f7973bd349a81a13d401af8d12f81801d6799fe6))
* re-implement RDFImporter ([e4e0d34](https://github.com/lu-pl/lodkit/commit/e4e0d347e5f5416fc9574b7640b42c12e296b5e6))
* rename type definitions ([dd06282](https://github.com/lu-pl/lodkit/commit/dd0628276ce1629890c48f7915103e2126d2c96f))


### Documentation

* add URIConstructor README section ([c69ff42](https://github.com/lu-pl/lodkit/commit/c69ff422efa841f0d46ace9fc3a35ca0d43f25ac))
* **readme:** remove README section about uriclass, make_uriclass ([fb15cfc](https://github.com/lu-pl/lodkit/commit/fb15cfc0a01eccb70bd9728a5c29c632753a5aa2))
* remove LODKit heading ([ae4cf83](https://github.com/lu-pl/lodkit/commit/ae4cf837718cd93ade1fd4792d16d47e4623690a))
* update README on RDFImporter ([1340b4f](https://github.com/lu-pl/lodkit/commit/1340b4f85bc05774320c9af18b596a97df40d59e))

## [0.4.0](https://github.com/lu-pl/lodkit/compare/v0.3.0...v0.4.0) (2025-12-01)


### Features

* implement TripleChain class ([2417670](https://github.com/lu-pl/lodkit/commit/241767084c3765e18e4215fb8e16fab22a0861d4))


### Documentation

* add TripleChain README section ([dd284da](https://github.com/lu-pl/lodkit/commit/dd284da1259821781239de38ce27afc7615e1fc9))
