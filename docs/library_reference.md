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
    - [all?](#all?)
    - [find](#find)
    - [contains](#contains?)
    - [present?](#present?)
    - [empty?](#empty?)
    - [concat](#concat)
    - [sort](#sort)
    - [join](#join)
  - [Dictionary[K, V]](#dictionary)
  	- [length](#length)
    - [contains?](#contains?)
    - [keys](#keys)
    - [values](#values)
    - [present?](#present?)
    - [empty?](#empty?)
  - [Set[T]](#set)
    - [length](#length)
    - [contains?](#contains?)
    - [union](#union)
    - [intersection](#intersection)
    - [present?](#present?)
    - [empty?](#empty?)
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
    - [center](#center)
    - [present?](#present?)
    - [empty?](#empty?)
    - [contains?](#contains?)
    - [to_int](#to_int)
    - [pad_left](#pad_left)
    - [pad_right](#pad_right)
  - [Int](#int)
    - [to_float](#to_float)
  - [Float](#float)
    - [to_int](#to_int)
- [functions](#functions)
  - [math](#math)
    - [ln](#ln)
    - [cos](#cos)
    - [tan](#tan)
    - [sin](#sin)
    - [cot](#cot)
  - [io](#io)
    - [display](#display)
    - [read](#read)
  - [system](#system)
    - [args](#args)
    - [arg_count](#arg_count)
    - [index](#index)
  - [regex](#regexp)
    - [compile](#compile)
    - [escape](#escape)

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

### sort

```javascript
List#sort() -> Void
```

sorts in place


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

### present?

```javascript
Dictionary#present?() -> Boolean
```

### empty?

```javascript
Dictionary#empty?() -> Boolean
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

### present?

```javascript
Set#present?() -> Boolean
```

```javascript
Set#empty?() -> Boolean
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

### substr_from

```javascript
String#substr_from(from: Int) -> String
```

### substr_to

```javascript
String#substr_to(to: Int) -> String
```

### length

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

### center

```javascript
String#center(count: Int, fill: String) -> String
```

### present?

```javascript
String#present?() -> Boolean
```

### empty?

```javascript
String#empty?() -> Boolean
```

### to_int

```javascript
String#to_int() -> Int
```

### pad_left

```javascript
String#pad_left(count: Int, fill: String) -> String
```

### pad_right

```javascript
String#pad_right(count: Int, fill: String) -> String
```

## Int

### to_int

```javascript
Int#to_int() -> Int
```

### to_float

```javascript
Int#to_float() -> Float
```

# functions

## math

Currently just several methods, add more in future versions
and investigate edge cases

### ln

```javascript
ln(x: Number) -> Float
```

the natural logarithm of x

### log

```javascript
log(x: Number, base: Number) -> Float
```

### cos

```javascript
cos(x: Number) -> Float
```

the cosine of x

### tan

```javascript
tan(x: Number) -> Float
```

the tangent

### sin

```javascript
sin(x: Number) -> Float
```

## io

### display

```javascript
display(*args: Any) -> Void
```

writes the contents to STDOUT using the native print function. `display` is the only pseudo
function accepting a variable number of args

### read

```javascript
read() -> String
```

reads a line from STDIN

## system

### args

```javascript
args() -> List[String]
```

returns a list with all the command line args

### arg_count

```javascript
arg_count() -> Int
```

returns the number of command line args (including the filename)

### index

```javascript
index(a: Int) -> String
```

a-th command arg, 1-based indexing(filename is 0)
