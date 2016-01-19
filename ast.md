
- [module](#module)
- [local](#local)
- [literals](#literals)
  - [int](#int)
  - [float](#float)
  - [string](#string)

# module

contains a module of code, corresponding to a single file/snippet

```python
Module
  code: list[Function / Class / Expression]
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

