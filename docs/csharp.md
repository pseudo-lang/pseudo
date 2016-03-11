C#
---

* support for all Pseudo v0.2 features
* [generator](../pseudo/generators/csharp_generator.py) [api translator](../pseudo/api_translators/csharp_translator.py) [tests](../tests/test_csharp.py)
* target version: C# 4+

C# equivalents used for pseudo types and concepts:


| Pseudo           | C#                                     |
|------------------|----------------------------------------|
| List[T]          | List\<T\>                      	    |
| Dictionary[K, V] | Dictionary\<K, V\>                     |
| Set[T]           | Set\<T\>                               |
| Tuple[T1, T2..]  | a custom class or Tuple\<T1, T2..\>    |
| Array[T, count]  | T[]                                    |
| Int              | int                                    |
| Float            | float                                  |
| String           | string                                 |
| for-loops        | foreach, for                           |
| classes          | classes                                |
| methods          | methods                                |
| functions        | static methods of main class           |


# niceties

* Converting tuples to classes and automatically inferring meaningful names for them based on usage in the program: e.g. in [football.cs](../examples/football.py):
  
  ```python
  return line[:away_index - 3], line[away_index:result_index - 1], (int(goals[0]), int(goals[1]))
  ```
  Pseudo detects a candidat-tuple with field types: String,  String and another candidat-tuple

  ```python
  return sum(result_points(team, *result) for result in results)
  ```

  The pseudo type of `result` is inferred to be `List[Tuple[String, String], Tuple[Int, Int]]`, so probably `result` is OK for a name of its class. Also all fields or result are passed to `result_points`

  ```python
  def result_points(team, host, away, goals):
  ```
  
  so we can use `host`, `away` and `goals` as field names and finally we build a class node which pseudo later translates as:

  ```c#
  public class Result
  {
  		private readonly string host;
  		public string Host { get { return host; } }

  		private readonly string away;
  		public String Away { get { return away; } }

  		private readonly Tuple<int, int> goals;
  		public Tuple<int, int> { get { return goals; } }

  		public Result(string host, string away, Tuple<int, int> goals)
  		{
  			this.host = host;
  			this.away = away;
  			this.goals = goals;
  		}
  }
  ```

  That analysis is done in Pseudo on the input pseudo syntax tree,
  the python code given here can be compiled to equivalent pseudo ast using [pseudo-python](https://github.com/alehander42/pseudo-python)


* Converting map/filter/other enumerable operations to LINQ methods

* Converting class attributes to either fields or properties analyzing their usage with `AttrAccessAnalyzeMiddleware`



