# go

* support: everything except for error handling
* [generator](https://github.com/alehander42/pseudo/tree/master/pseudo/generators/golang_generator.py) [api translator](https://github.com/alehander42/pseudo/tree/master/pseudo/api_translators/golang_translator.py) [tests](https://github.com/alehander42/pseudo/tree/master/tests/test_go.py)
* target version: Go 1.2+

Go equivalents used for pseudo types and concepts:

| Pseudo     | Go                   |
|------------|----------------------|
| List[T]          | slice[T]                             |
| Dictionary[K, V] | map[K]V                              |
| Set[T]           | map[bool]struct{}                    |
| Tuple[T1, T2..]  | a custom struct                      |
| Array[T, count]  | T[count]                             |
| Int              | int                                  |
| Float            | float                                |
| String           | string                               |
| for-loops        | for                                  |
| classes          | structs                              |
| methods          | struct methods                       |

## error handling

error handling is currently not supported for go.

it's going to be supported in v0.3 and almost everything is ready for that:
  there's a sketchup of the GoErrorHandlingMiddleware that's going to
  transform exception-based code to return-errors-based code
  it will probably reuse some of the leaking handlers logic, because for
  e.g.

```python
def process_pair(a, b):
    return process(parse_int(a), parse_float(b)).result
```

where `parse_x` throws `ParseError` and `process` throws `WatError` we'll need to inject error handling code in the surrounding block:

```go
func ProcessPair(a string, b string) Result {
    parsed_a, err := parse_int(a)
    if err {
        return nil, err
    }
    parsed_b, err := parse_float(b)
    if err {
        return nil, err
    }
    processed, err := process(parsed_a, parsed_b)
    if err {
    	return nil, err
    }
    return processed.result
}
```

not really beautiful, but hey, we're not letting those evil errors go away /s


