# Example 1: Fibonacci

[Pseudo AST](fib.pseudo.yaml)

Generated from [original.py](original.py) using [pseudo-python](https://github.com/alehander42/pseudo-python)


 to [VerbalExpressions](https://github.com/VerbalExpressions/PythonVerbalExpressions)

It defines a DSL for more readable definition of regular expressions and uses it with the example from [VerbalExpressions README](https://github.com/VerbalExpressions/PythonVerbalExpressions)

It demonstrates 

* Type inference

* Native standard library use: Pseudo uses the target language
standard library print function

* Syntax translation

* Even if you are making a cat-based psychosomatic compiler targeting elvish slangs, you have a fibonacci example
 
The next two examples: [football](../football) and [verbal_expressions](../verbal_expressions) are way more interesting

Commands: (assuming you're in `examples/fib`)

* python

    translate to py with
    ```bash
    # from python source
    > pseudo-python original.py fib.py
    #or from ast
    > pseudo fib.pseudo.yaml py
    ```


    and run with
    ```
    > python fib.py
    ```

* javascript
    
    translate to js with
    ```bash
    # from python source
    > pseudo-python original.py fib.js
    #or from ast
    > pseudo fib.pseudo.yaml js
    ```

    and run with
    ```bash
    > node fib.js
    ```

* ruby

    translate to ruby with

    ```bash
    # from python source
    > pseudo-python original.py fib.rb
    #or from ast
    > pseudo fib.pseudo.yaml rb
    ```

    and run with
    ```bash
    > ruby fib.rb
    ```

* c#
    
    translate to c# with

    ```bash
    # from python source
    > pseudo-python original.py fib.cs
    #or from ast
    > pseudo fib.pseudo.yaml csharp
    ```

    and run with
    ```bash
    > mcs fib.cs # or an equivalent command compiling cs files
    > ./fib.exe
    ```

* go
    
    translate to go with

    ```bash
    # from python source
    > pseudo-python original.py fib.go
    #or from ast
    > pseudo fib.pseudo.yaml go
    ```

    and run
    ```bash
    > go run fib.go
    ```
