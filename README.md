[![Build Status](https://travis-ci.org/alehander42/pseudo.svg?branch=master)](https://travis-ci.org/alehander42/pseudo)
[![codecov.io](https://codecov.io/github/alehander42/pseudo/coverage.svg?branch=master)](https://codecov.io/github/alehander42/pseudo?branch=master)
[![MIT License](http://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

# pseudo

Pseudo is a library for generating code in different high level languages and a system for language translation: its goal is to be able to translate any code expressed in a certain "pseudo-translateable" subset of each supported language or as a pseudo AST to readable and idiomatic code in any of the supported target languages. 

Pseudo achieves that with translation on two layers: it uses the target language syntax and it can express standard library methods/api of language X using language Y's native standard library

Pseudo specifies an ast format corresponding to a very clear and somehow limited subset of a language:

  * basic types and collections and standard library methods for them
  
  * integer, float, string, boolean
  * lists
  * dicts
  * sets
  * tuples/structs(fixed length heterogeneous lists)
  * fixed size arrays
  * regular expressions

  * functions with normal parameters (no default/keyword/vararg parameters)
  * classes 
    * single inheritance
    * polymorphism
    * no dynamic instance variables
    * basically a constructor + a collection of instance methods, no fancy metaprogramming etc supported

  * exception-based error handling with support for custom exceptions
  (target languages support return-based error handling too)
  
  * io: print/input, file read/write, system and subprocess commands

  * iteration (for-in-range / for-each / iterating over several collections / while)
  * conditionals (if / else if / else)
  * standard math/logical operations

[ast reference](docs/ast.md)
[standard library reference](docs/library_reference.md)


Those constructs and entities have almost the same behavior and very same-spirited api in a lot of the languages which Pseudo would support.

## use cases

  * generate code for the same task/algorithm in different languages (parser generators etc)
  * port a library/codebase
  * develop core logic in one language and use it in other language codebases
  * write a compiler/dsl
  * bootstrap a codebase in another language / generate equivalent test suites in different languages
  * translate/support some algorithms in different languages
  * translate/support some text/data processing/command tool in different languages

## why

Supporting full-blown Ruby to Python/Javascript to C++ auto translation is hard.
However often we need to just exress the core

Often that code is(or can be) expressed in very similar way, with
similar constructs and basic types and data structures. On that level
a lot of languages are very similar and the only real difference
is syntax and methods api. That's a feasible task for automatic translation
and actually the existance of `pseudo` is to fullfill the needs of several other
existing projects.

You can almost think of it in a "~json-for-algorithms" way: we express
our algorithm/function with standard basic types, collections and constructs in our favorite language or in pseudo AST format and we can translate to any of the supported target languages.

You can also use the "lodash-with-babylon-fishes" metaphor: we use e.g. Python or Ruby or Pseudo standard library and Pseudo maps uses the right equivalent idioms in the target language.


## progress

close to v0.2, left: several fixes and finishing the api translation

- [ ] python
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] ruby
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] javascript
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] c#
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] c++
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] go
  - [x] syntax tests passing
  - [ ] api tests passing
- [ ] php
  - [ ] syntax tests passing
  - [ ] api tests passing
 
## Target languages

- [x] python
- [x] ruby

- [x] javascript
- [x] c#
- [x] c++
- [x] go
- [ ] php

v0.3/v0.4:

- [ ] java
- [ ] perl

- [ ] swift ?
- [ ] c ?

- [ ] clojure ?

## Language support

Using pseudo's DSL it's easy to add support for a new language, so it's feasible to expect support for most popular languages and even different versions of them (e.g. EcmaScript 6/7, Perl 5/6 Java 7 / 8)

## How to translate back?

Currently there are `python`, `js` and `c#` to `pseudo` compilers in the works

## Intermediate AST format

The AST format uses basic data structures available in most languages. The nodes correspond to 
dictionaries with `type` key corresponding to the node type and `field_name` keys corresponding to
the node fields, similar to the widely popular `estree` ecmascript format.

Pseudo can consume ast either serialized in `.pseudo.yaml` files or directly as
dictionary objects through it's `pseudo.generate(ast, output_lang)` API

## Implementation

The implementation goal is to make the definitions of new supported languages  really clear and simple. If you dive in, you'll find out
almost all the code/api transformations are defined using a declarative dsl with rare ocassions 
of edge case handling helpers. That has a lot of advantages:
* Less bugs: the core transformation code is really generalized, it's reused as a dsl and its results are well tested
* Easy to comprehend: it almost looks like a config file
* Easy to add support for other languages: I was planning to support just python and c# in the initial version but it is so easy to add support for a language similar to the current supported ones, that I
added support for 4 more.
* Easy to test: there is a simple test dsl too which helps all language tests to share input examples [like that](pseudo/tests/test_ruby.py)

## Target language specific docs

* [python](docs/python.md)
* [c#](docs/csharp.md)
* [go](docs/go.md)
* [ruby](docs/ruby.md)
* [javascript](docs/javascript.md)
* [c++](docs/cpp.md)
* [php](docs/php.md)

## License

Copyright © 2015 2016 Alexander Ivanov

Distributed under the MIT License.
