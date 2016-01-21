## types

pseudon supports fully dynamic languages so we don't **require** any type signatures.
however most of our use cases have been for pure algorithms or for generating code
for a certain taks. in both cases the code isn't too dynamic and you can easily apply
type signatures to it. most of the time it's useful for pseudon to have at least some awareness about
the types of the names in the ast in order to translate into the right standard
target language methods/functions. we group the cases in 3 categories:

* custom class attributes / methods

e.g. 
```ruby
Person.name
Person.age = 2
Person.full_name({capitalize: false})
```

the custom classes themselves should be defined somewhere in the input code and their 
attributes and methods will always be translated by Pseudon to something equivalent, so
everything is pretty straightforward 

* sequences

e.g.
```python
'w' + 'a'
[2] + [4]
2 + 4
```

here it's quite important to know if we do integer addition, list or string concatenation.
For example in php those 3 should translate to

```php
"w" . "a";
array_concat([2], [4]);
2 + 4;
```

so you can see why do we need to be aware of them. It was a very complicated decision, because the easiest thing for Pseudon is to leave the responsibillity of type hinting everything to `xlang-pseudon` clients.
The worry was the Pseudon can apply that logic once, but then you have different clients emitting incompatible code and all of them depending on the central implementation to have internal knowledge about the quirks of each of them. That's why currently each of the clients is expected to either use it's language
type system or to infer types of the pseudon-translateable code itself.
That may sound hard but the type system for pseudon is pretty basic and soft. 
Also that's already implemented in `pseudon-python`, `pseudon-ruby` and `pseudon-js`, and soon in 
`pseudon-php`, so if anybody is interested in developing `pseudon-<another-dynamic-l>`
one can always take a look to those implementations or to ask in the issues/maintainer email.


