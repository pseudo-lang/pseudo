## Examples: football

[Pseudo AST](football.pseudo.yaml)

Generated from [football.py](https://github.com/alehander42/pseudo-python/blob/master/examples/football.py) using [pseudo-python](https://github.com/alehander42/pseudo-python)

That's a simple command line program that

* accepts a filename and a team name specified by command args
* shows a "usage" message if not enough command args are supplied
* reads the file specified by the filename
* parses the football results in it
* calculates the points that the team has accumulated based on its results

It demonstrates 

* native standard library use: Pseudo uses the target language
standard library string/list methods/functions
* idiomatic code translation: e.g. in the `C#` version Pseudo analyzes the use of a tuple and generates and uses a class with suitable field names instead
* I/O handling: Pseudo uses the target language standard library to do file I/O and print data
* index/length of command args based on target language conventions, handy for little command line tools
    
    * [js](football.js)
      2-based command args

      ```javascript
      if (process.argv.length < 4) {`
      ```

      ```javascript
      var results = load_results(process.argv[2]);
      ```
    * [c#](football.cs)
      0-based command args

      ```c#
      if (args.Length < 2)
      ```

      ```c#
      var results = LoadResults(args[0]);
      ```

    * [python](football.py)
      1-based command args

      ```python
      if len(sys.argv) < 3:
      ```

      ```python
      results = load_results(sys.argv[1])
      ```


Commands:

* python

    ```bash
    > pseudo football.pseudo.yaml py
    > python football.py football.txt Liverpool 
    6
    ```

* javascript

    ```bash
    > pseudo football.pseudo.yaml js
    > node football.js football.txt Liverpool 
    6
    ```

* ruby

    ```bash
    > pseudo football.pseudo.yaml rb
    > ruby football.rb football.txt Liverpool 
    6
    ```

* c#
    
    ```bash
    > pseudo football.pseudo.yaml csharp
    > mcs football.cs # or an equivalent command compiling cs files
    > ./football.exe football.txt Liverpool
    6
    ```

