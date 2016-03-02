# pseudon

Pseudon is a library for generating code in different high level languages and a system for language algorithm translation: its goal is to be able to translate any code expressed in a certain "pseudon-translateable" subset of each supported language or as a pseudon AST to any of the supported target languages.

Supporting full-blown X to Y auto translation is hard. 

However Pseudon support a very clear and somehow limited subset of a language:

  * basic types: integer, float, string, boolean, nil
  * lists
  * dicts
  * standard library methods for the basic types
  * functions with normal parameters (no default/keyword/vararg parameters)
  * classes (only as a constructor + a collection of instance methods, no fancy metaprogramming etc supported)
  * iteration (for-in loops / while)
  * conditionals (if / else if / else)
  * standard math/logical operations
  * basic exception-based error handling


Those constructs and entities have almost the same behavior and very same-spirited api in a lot of the dynamic languages which Pseudon would support.

##why
Supporting full-blown Ruby to Python/Perl to Javascript auto translation is hard.
However often we need to

  * translate/support some algorithms in different languages
  * translate/support some text/data processing tool in different languages
  * generate code for the same task/algorithm in different languages

Often that code is(or can be) expressed in very similar way, with
similar constructs and basic types and data structures. On that level
a lot of dynamic languages are very similar and the only real difference
is syntax and methods api. That's a feasible task for automatic translation
and actually the existance of `pseudon` is to fullfill the needs of other
existings projects.

You can almost think of it in a "~json-for-algorithms" way: we express
our algorithm/function with standard basic types, collections and constructs in our favorite language 
or in pseudon AST format and we can translate to any of the supported target languages

## Target languages

- [x] python
- [x] ruby

- [ ] javascript
- [ ] c#
- [ ] c++
- [ ] go
- [ ] php

next version:

- [ ] java
- [ ] perl

- [ ] swift ?
- [ ] c ?

## How to translate back?

Each language is supposed to have its own pseudon generator. 

* [pseudon-ruby](https://github.com/alehander42/pseudon-ruby)
* [pseudon-python](https://github.com/alehander42/pseudon-python)
* [pseudon-js](https://github.com/alehander42/pseudon-js)

## Intermediate AST format

The AST format uses basic data structures available in most languages. The nodes correspond to 
dictionaries with `type` key corresponding to the node type and `field_name` keys corresponding to
the node fields, similar to the widely popular `estree` ecmascript format.

Pseudon can consume ast either serialized in `.pseudon.yaml` / `.pseudon.json` files or directly as
dictionary objects through it's `pseudon.generate(ast, output_lang)` API

The first prototype of pseudon was using lisp-like code, but standard data formats seemed like the
more easy-to-approach for users solution

## Implementation

The implementation goal is to be really clear and simple. If you dive in, you'll find out
almost all the code/api transformations are defined using a declarative dsl with rare ocassions 
of edge case handling helpers. That has a lot of advantages:
* Less bugs: the core transformation code is really generalized, it's reused as a dsl and its results are well tested
* Easy to comprehend: it almost looks like a config file
* Easy to add support for other languages: I was planning to support just python and c# in the initial version but it is so easy to add support for a language similar to the current supported ones, that I
added support for 5 more.
* Easy to test: there is a simple test dsl too which helps all language tests to share input examples and I mean [just look](pseudon/tests/test_javascript.py) at it

[progress](progress.md)

## License

Copyright © 2015 2016 Alexander Ivanov

Distributed under the MIT License.
