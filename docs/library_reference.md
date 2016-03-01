- [methods](#methods)
  - [List[T]](#list)
    - [push](#push)
  - [Dictionary[K, V]](#dictionary)
    - [setitem](#setitem)
- [functions](#functions)
  - [math](#math)
    - [log](#log)
  - [io](#io)
    - [display](#display)

# methods

## List

```python
List[T]
```

### push

```python
push(element: T) -> Void
```

pushed an element at the end of the list

## Dictionary

```python
Dictionary[K, V]
```

### setitem

```python
setitem(key: K, value: V) -> Void
```

set/update the value corresponding to key, usually equivalent to `[key] = value`

# functions

## math

### log

```python
log(x: Number, base: Number) -> Float
```

the logarithm of x to the given base

## io

### display

```python
display(*args: Any) -> Void
```

displays the contents on the screen using the native print function. `display` is the only pseudon
function accepting a variable number of args



