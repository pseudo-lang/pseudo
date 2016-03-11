# c++

* experimental support: most of api still not supported
* [generator](../pseudo/generators/cpp_generator.py) [api translator](../pseudo/api_translators/cpp_translator.py) [tests](../tests/test_cpp.py)
* target version: C++11

C++ equivalents used for pseudo types and concepts:


| Pseudo           | C++                     |
|------------------|-------------------------|
| List[T]          | vector<T>               |
| Dictionary[K, V] | unordered_map<K, V>     |
| Set[T]           | set<T>                  |
| Tuple[T1, T2..]  | tuple<T1, T2..>         |
| Int              | int                     |
| Float            | float                   |

## niceties

* support c++ lambdas
* uses `smart_ptr` and `weak_ptr` instead of raw pointers, thanks to CppPointerMiddleware
