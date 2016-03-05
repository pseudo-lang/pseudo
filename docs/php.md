# php

* support
* [generator](../pseudo/generators/php_generator.py) [api translator](../pseudo/api_translators/php_translator.py) [tests](../tests/test_php.py)
* target version: PHP5.4

PHP equivalents used for pseudo types and concepts:


| Pseudo           | PHP                     |
|------------------|-------------------------|
| List[T]          | array                   |
| Dictionary[K, V] | array                   |
| Set[T]           | array with boolean values |
| Tuple[T1, T2..]  | array                   |
| Int              | int                     |
| Float            | float                   |

## niceties

* support new php array literals