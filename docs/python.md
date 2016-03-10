# python

* full support
* [generator](../pseudo/generators/python_generator.py) [api translator](../pseudo/api_translators/python_translator.py) [tests](../tests/test_python.py)
* target version: Python3.2+

Currently `pseudo` targets Python3.2+ . It's easy to add Python2.7+ support too,
most of the tests/generator and api translation would be shared and we might need some unicode-code-handling pseudo middleware

Python equivalents used for pseudo types and concepts:

| Pseudo           | Python |
|------------------|--------|
| List[T]          | list   |
| Dictionary[K, V] | dict   |
| Set[T]           | set    |
| Tuple[T1, T2..]  | tuple  |
| Array            | tuple  |
| Int              | int    |
| Float            | float  |
| String 		   | str    |
| for-loops        | for    |
| classes          | classes|
| methods          | methods|
| functions        | funcs  | 


# niceties

* Converting map/filter/other enumerable operations to list/dict/set comprehensions depending on return type

* Converting private methods names to _method_name (in v0.3 private attr and method names would be configurable from pseudo_config.yaml)

