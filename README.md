# pseudon

Pseudon is a system for dynamic language algorithm translation: its goal is to be able to translate any code expressed in a certain "pseudon-translateable" subset of each supported language to any of the others.

Pseudon will support a very clear and somehow limited subset of a language:

  * basic types: integer, float, string, boolean, nil
  * lists
  * dicts
  * standard library methods for the basic types
  * classes (only as collection of instance methods, no fancy metaprogramming supported)

They have almost the same behavior and very same-spirited api in a lot of the dynamic languages Pseudon would support.

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
and actually the existance of `pseudon` is to fullfill a need of another
existing project.

You can almost think of it in a "~json-for-algorithms" way: we express
our code with standard basic types, collections and simple classes and we can translate to a common format and using it as a middle ground between each supported language

## Target languages

* py (python)
* rb (ruby)
* js (javascript)
* pl (perl)

## How to translate back?

Each language has its own pseudon generator

* [pseudon-ruby](https://github.com/alehander42/pseudon-ruby)
* [pseudon-python](https://github.com/alehander42/pseudon-python)
* [pseudon-perl](https://github.com/alehander42/pseudon-perl)

## Intermediate format

The first prototype of pseudon was using lisp-like code, but the current version
uses yaml. 

## Implementation



## License

Copyright © 2015 Alexander Ivanov

Distributed under the MIT License.
