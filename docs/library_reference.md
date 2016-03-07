- [methods](#methods)
  - [List[T]](#list)
    - [push](#push)
    - [pop](#pop)
    - [length](#length)
    - [insert](#insert)
    - [remove](#remove)
    - [remove_at](#remove_at)
    - [slice](#slice)
    - [slice_from](#slice_from)
    - [slice_to](#slice_to)
    - [map](#map)
    - [filter](#filter)
    - [reduce](#reduce)
    - [any?](#any?)
  - [Dictionary[K, V]](#dictionary)
  	- [length](#length)
    - [contains?](#contains?)
    - [keys](#keys)
    - [values](#values)
  - [Set[T]](#set)
    - [length](#length)
    - [contains?](#contains?)
    - [union](#union)
    - [intersection](#intersection)
- [functions](#functions)
  - [math](#math)
    - [log](#log)
  - [io](#io)
    - [display](#display)

# methods

## List

```javascript
List[T]
```

### push

```javascript
List#push(element: T) -> Void
```

pushes an element at the end of the list

### pop

```javascript
List#pop() -> T
```

pops the last element of the list, undefined behavior for empty lists

### length

```javascript
List#length() -> Int
```

### insert

```javascript
List#insert(element: T, index: Int) -> Void
```

### remove

```javascript
List#remove(element: T) -> Void
```

### remove_at

```javascript
List#remove_at(index: Int) -> Void
```

### slice

```javascript
List#slice(from: Int, to: Int) -> List[T]
```

### slice_from

```javascript
List#slice_from(from: Int) -> List[T]
```

### slice_to

```javascript
List#slice_to(to: Int) -> List[T]
```

### map

```javascript
List#map(f: Function[T, Z]) -> List[Z]
```

### filter

```javascript
List#filter(f: Function[T, Boolean]) -> List[T]
```

### reduce

```javascript
List#reduce(f: Function[T, Z, Z], initial: Z) -> Z
```

### any?

```javascript
List#any?(f: Function[T, Boolean]) -> Boolean
```

### all?

```javascript
List#all?(f: Function[T, Boolean]) -> Boolean
```


## Dictionary

```javascript
Dictionary[K, V]
```

### length

```javascript
Dictionary#length() -> Int
```
### contains?

```javascript
Dictionary#contains?() -> Boolean
```

# functions

## math

### log

```javascript
log(x: Number, base: Number) -> Float
```

the logarithm of x to the given base

## io

### display

```javascript
display(*args: Any) -> Void
```

displays the contents on the screen using the native print function. `display` is the only pseudo
function accepting a variable number of args



