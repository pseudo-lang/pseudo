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
  - [Tuple[T1, T2..]](#tuple)
    - [length](#length)
  - [Array[T, length]](#array)
    - [length](#length)
  - [String](#string)
    - [substr](#substr)
    - [substr_from](#substr_from)
    - [substr_to](#substr_to)
    - [length](#length)
    - [concat](#concat)
    - [find](#find)
    - [count](#count)
    - [partition](#partition)
    - [split](#split)
    - [trim](#trim)
    - [reversed](#reversed)
    - [justify](#justify)
    - [c_format](#c_format)
    - [format](#format)

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
Dictionary#contains?(element: T) -> Boolean
```

### keys

```javascript
Dictionary#keys() -> List[K]
```

### values

```javascript
Dictionary#values() -> List[V]
```

## Set[T]

### length

```javascript
Set#length() -> Int
```

### contains?

```javascript
Set#contains?(element: T) -> Boolean
```

### union

```javascript
Set#union(right: Set[T]) -> Set[T]
```

### intersection

```javascript
Set#intersection(right: Set[T]) -> Set[T]
```

## Tuple[T1, T2..]

### length

```javascript
Tuple#length() -> Int
```

## Array[T, length]

### length

```javascript
Array#length() -> Int
```

## String

### substr

```javascript
String#substr(from: Int, to: Int) -> String
```

```javascript
String#substr_from(from: Int) -> String
```

```javascript
String#substr_to(to: Int) -> String
```

```javascript
String#length() -> Int
```

### concat

```javascript
String#concat(value: String) -> String
```

### find

```javascript
String#find(element: String) -> Int
```

### count

```javascript
String#count(element: String) -> Int
```

### partition

```javascript
String#partition(on: String) -> Tuple[String, String]
```

### split

```javascript
String#split(delimiter: String) -> List[String]
```

### trim

```javascript
String#trim() -> String
```

### reversed

```javascript
String#reversed() -> String
```

### justify

```javascript
String#justify() -> String
```

### c_format

```javascript
String#c_format(*args: Any) -> String
```

formats using c-style `%d`, `%f`, `%s` etc, function accepting a variable number of args

### format

```javascript
String#format(*args: Any) -> String
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



