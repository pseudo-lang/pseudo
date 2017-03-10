v0.3/v0.4:

Main goals:

* Implement fully the initial version of the pseudo standard library
* Test generated code using the target runtime / compilers
* Fix C++ support, add initial support for Swift, Java and Nim as targets
* Finish "functional" mode and add initial support for Haskell
* 1-2 more non-trivial apps using Pseudo-Python

pseudo-python:

* Implement full support for the pseudo-translatable syntax
* Add a lot more tests
* Support everything from the standard library that is translatable to the v0.3 pseudo standard library (and only that, pseudo-python's goal **is not to support fully python or the standard library**, that's very important because we want to reuse pseudo-python's approach and design for pseudo-js etc)
* Eventually support some kind of mockups / hints to ease translating just a part of an existing codebase

v0.5:

* Support some form of concurrency
* Support the concept of multiple files, folder/library structure
and generate idiomatic `gem`/`npm package`/`go`/`c#` folder structures
* Work on the next pseudo-<lang> compiler after pseudo-python: pseudo-js / pseudo-ruby ?

pseudo-python

* Add more capabilities to the type system ?
* Infer purity of functions?
