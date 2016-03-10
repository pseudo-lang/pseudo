# javascript

* full support
* [generator](../pseudo/generators/js_generator.py) [api translator](../pseudo/api_translators/js_translator.py) [tests](../tests/test_javascript.py)
* target version: Ecmascript 5

JavaScript equivalents used for pseudo types and concepts:


| Pseudo           | JavaScript              |
|------------------|-------------------------|
| List[T]          | Array                   |
| Dictionary[K, V] | Object 			     |
| Set[T]           | Object with boolean values|
| Tuple[T1, T2..]  | Array                   |
| Array            | Array                   |
| Int              | Number                  |
| Float            | Number                  |
| String 		   | String                  |
| for-loops        | for, _.each             |
| classes          | objects and prototypical inheritance  |
| methods          | prototype functions     |
| functions        | functions               |

## standard library

We use some standard javascript methods (`.splice`, `.slice`, `Math...`), `node.js` standard library (`File`) and `lodash`.
JavaScript doesn't really have the equivalent of a all-implementations-use-it standard library historically, and `lodash` or `underscore` are widely used to fill that gap for a lot of base type methods, so that was a good match for pseudo's goal.
In the future `pseudo` might add support for different JS api translators targeting/using different libraries/your own library

## ecmascript version

Currently Ecmascript 5 is the most popular version, so that's what pseudo targets. Actually ES6/ES7/Coffeescript/Typescript are
closer semantically and have a richer choice of builtin types/language structures, so they would be even easier to support in next versions.


## future versions

`io:read` is not currently supported, because it's typically equivalent
to a callback for the `stdin` stream in Node. 
Pseudo would support callback-based js api-s from v0.3 or v0.4
