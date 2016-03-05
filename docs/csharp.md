# c\#

* support
* [generator](https://github.com/alehander42/pseudo/tree/master/pseudo/generators/csharp_generator.py) [api translator](https://github.com/alehander42/pseudo/tree/master/pseudo/api_translators/csharp_translator.py) [tests](https://github.com/alehander42/pseudo/tree/master/tests/test_csharp.py)
* target version: C# 4+

C# equivalents used for pseudo types and concepts:


| Pseudo           | C#                   |
|------------------|----------------------|
| List[T]          | List\<T\>            |
| Dictionary[K, V] | Dictionary\<K, V\>   |
| Set[T]           | Set\<T\>             |
| Tuple[T1, T2..]  | Tuple\<T1, T2..\>    |
| Int              | int                  |
| Float            | float                |

# niceties

* Converting map/filter/other enumerable operations to LINQ methods

* Converting class attributes to either fields or properties analyzing their usage with `AttrAccessAnalyzeMiddleware`





