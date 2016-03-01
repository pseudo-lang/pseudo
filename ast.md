
- [module](#module)
- [literals](#literals)
  - [int](#int)
  - [float](#float)
  - [string](#string)
  - [none](#none)
  - [list](#list)
  - [dict](#dict)
- [idents](#idents)
  - [local](#local)
  - [typename](#typename)
  - [instance_variable](#instance_variable)
  - [attr](#attr)
- [assignments](#assignments)
  - [local_assignment](#local_assignment)
  - [instance_assignment](#instance_assignment)
  - [attr_assignment](#attr_assignment)
- [calls](#calls)
  - [call](#call)
  - [method_call](#method_call)
  - [standard_call](#standard_call)
  - [standard_method_call](#standard_method_call)
- [operations](#operations)
  - [binary_op](#binary_op)
  - [unary_op](#unary_op)
  - [comparison](#comparison)
- [control flow](#control flow)
  - [if](#if_statement)
  - [for_each](#for_each_statement)
  - [for_range](#for_range_statement)
  - [for_each_with_index](#for_each_with_index_statement)
  - [for_each_in_zip](#for_each_in_zip_statement)
  - [while](#while_statement)
  - [switch](#switch_statement)
- [functions](#functions)
  - [function_definition](#function_definition)
  - [method_definition](#method_definition)
  - [anonymous_function](#anonymous_function)
- [classes](#classes)
  - [class_definition](#class_definition)
  - [this](#this)
  - [constructor](#constructor)


# module

contains a module of code, corresponding to a single file/snippet

```python
Module
  code: [Function / Class / Expression]
```

```python
42
```

```yaml
type: module
code:
  - type: int
    value: 42
``` 

# literals

## int

contains an int

```python
Int
  value: int
```

```python
42
```

```yaml
type: int
value: 42
```

## float

contains a float

```python
Float
  value: float
```

```python
4.2
```

```yaml
type: float
value: 4.2
```

## string

contains a string

```python
String
  value: str
```

```python
'eyes'
```

```yaml
type: string
value: eyes
```

## none

contains none value

```python
None
```

```python
None
```

```yaml
type: none
```

## list

contains a list literal

```python
List
  elements: [Expression]
```

```python
[42, None]
```

```yaml
type: list
elements:
  - type: int
    value: 42
  - type: none
```

## dict

contains a dictionary literal, the keys are supposed to be numbers or strings or booleans so
most target languages can support them natively.

```python
Dict
  pairs: [[Hashable, Expression]]
```

```python
{v: v}
```

```yaml
type: dict
pairs:
  -
    - type: local
      name: v
    - type: local
      name: v
```

# idents

## local

usually a local variable or an argument to the current function

```python
Local
  name: str
```

```python
e #python
```

```ruby
e #ruby
```

```yaml
type: local
name: e
```

## typename

usually the name of a class or type

```python
Typename
  name: str
```

```python
Animal
```

```yaml
type: typename
name: Animal
```

## instance_variable

an instance variable accessed in a method of its class

```python
InstanceVariable
  name: str
```

```python
self.e #python
```

```ruby
@e #ruby
```

```yaml
type: instance_variable
name: e
```

## attr

an attribute of an object

```python
Attr
  receiver: Expression
  attr: str
```

```yaml
type: attr
receiver:
  type: int
  value: 2
attr: size
```

# assignments

## local_assignments

an assignment to a local variable (the usual kind of assignment).
```python
LocalAssignment
  local: str
  value: Expression
```

```python
e = 'eyes' 
x, y = 2, 4
```

multi assignments is also supposed to be represented as series of assignment nodes

```yaml
type: local_assignment
local: e
value:
  type: string
  value: eyes

type: local_assignment
local: x
value:
  type: int
  value: 2
type: local_assignment
local: y
value:
  type: int
  value: 2
```

## instance_assignment

an assignment of ivar

```python
InstanceAssignment
  name: str
  value: Expression
```

```python
self.e = e # python
```

```ruby
@e = e # ruby
```

```yaml
type: instance_assignment
name: e
value:
  type: local
  name: e
```

## attr_assignment

an assignment to attr

```python
AttrAssignment
  attribute: Attribute
  value: Expression
```

```python
a.i = None # python
```

```php
$a->i = NULL; # php
```

```yaml
type: attr_assignment
attribute:
  type: Attribute
  object: 
    type: local
    name: a
  name: i
value:
  type: none
```

# calls

## call

a function call

```python
Call
  function: Expression
  args: [Expression]
```

```python
analyze(e, 2)
```

```yaml
type: call
function:
  type: local
  name: analyze
args:
  - type: local
    name: e
  - type: int
    value: 2
```

## method_call

a call to an object's method

```python
MethodCall
  receiver: Expression
  message: str
  args: [Expression]
```

```python
h.analyze()
```
```yaml
type: method_call
receiver:
  type: local
  name: h
message: analyze
args: []
```

## standard_call

a call to a standard pseudon function
pseudon standard functions are divided in namespaces, they in a combination with standard methods (below) represent the pseudon standard library
the standard library corresponds to the only pseudon-translateable native functions and methods(builtin in the input/target language or its standard library)
if you want support for other functions/methods, please follow the [extend pseudon guide](docs/extend_pseudon_guide.md)

the namespaces currently are `global`(no namespace/top namespace) `math`, `io`, `system`
you can read more in [standard library reference](docs/library_reference.md)


```python
StandardCall
  namespace: None / str
  function: str
  args: [Expression]
```

```python
print(2)
```

```yaml
type: standard_call
namespace: io
function: display
args:
  - type: int
    value: 2
```

## standard_method_call

a pseudon standard library method call
the standard library corresponds to the only pseudon-translateable native functions and methods(builtin in the input/target language or its standard library)
if you want support for other functions/methods, please follow the [extend pseudon guide](docs/extend_pseudon_guide.md)

you can read more in [standard library reference](docs/library_reference.md)

```
python
StandardMethodCall
  receiver: Expression
  message: str
  args: [Expression]
```

```python
f()[1:] # f returns a list of int
```
```yaml
type: standard_method_call
receiver:
  type: call
    function:
      type: local
      name: f
    args: []
    pseudon_type: List[Int]
message: slice_from
args:
  - type: int
    value: 1
pseudon_type: List[Int]
```

