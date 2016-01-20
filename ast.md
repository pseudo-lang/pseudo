
- [module](#module)
- [local](#local)
- [literals](#literals)
  - [int](#int)
  - [float](#float)
  - [string](#string)
  - [none](#none)
  - [list](#list)
  - [dict](#dict)
- [assignments](#assignments)
  - [local_assignment](#local_assignment)
  - [instance_assignment](#instance_assignment)
  - [attr_assignment](#attr_assignment)

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

## local

contains a local name value, written in snake_case by convention

```python
Local
  name: str
```

```python
e
```

```yaml
type: local
name: 'e'
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
