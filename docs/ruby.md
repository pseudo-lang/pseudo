# ruby

* full support
* [generator](../pseudo/generators/ruby_generator.py) [api translator](../pseudo/api_translators/ruby_translator.py) [tests](../tests/test_ruby.py)
* target version: Ruby 2+

Ruby equivalents used for pseudo types and concepts:


| Pseudo           | Ruby                 |
|------------------|----------------------|
| List[T]          | Array                |
| Dictionary[K, V] | Hash                 |
| Set[T]           | Set                  |
| Tuple[T1, T2..]  | Array                |
| Array            | Array                |
| Int              | Int                  |
| Float            | Float                |
| String 		   | String, Symbol       |
| for-loops        | .each, .each_with_index         |
| classes          | classes              |
| methods          | methods              |
| functions        | methods in global scope|

# niceties

* Converting class attributes to `attr_accessor` / `attr_reader` / `attr_writer` 
after analyzing their usage with `AttrAccessAnalyzeMiddleware`

* Expressing array literals with ruby-specific magnificient `%w` / `%q` etc syntax based on their element types :

```
%w(ha oh well) 
%q(look at me fancy)
```






