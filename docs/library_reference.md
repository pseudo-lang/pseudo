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

```ruby
List[T]
```

### push

```ruby
List#push(element: T) -> Void
```

pushes an element at the end of the list

### pop

```ruby
List#pop() -> T
```

pops the last element of the list, undefined behavior for empty lists

### length

```ruby
List#length() -> Int
```

### insert

```ruby
List#insert(element: T, index: Int) -> Void
```

### remove

```ruby
List#remove(element: T) -> Void
```

### remove_at

```ruby
List#remove_at(element: T, index: Int) -> Void
```

### slice

```ruby
List#slice(from: Int, to: Int) -> List[T]
```

### map

```ruby
List#map(f: Function[T, Z]) -> List[Z]
```

## Dictionary

```ruby
Dictionary[K, V]
```

### setitem

```ruby
setitem(key: K, value: V) -> Void
```

set/update the value corresponding to key, usually equivalent to `[key] = value`

# functions

## math

### log

```ruby
log(x: Number, base: Number) -> Float
```

the logarithm of x to the given base

## io

### display

```ruby
display(*args: Any) -> Void
```

displays the contents on the screen using the native print function. `display` is the only pseudo
function accepting a variable number of args



