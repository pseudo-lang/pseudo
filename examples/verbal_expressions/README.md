# Example 2: Verbal expressions

[Pseudo AST](verbal_expressions.pseudo.yaml)

Generated from [verbal_expressions](https://github.com/alehander42/pseudo-python/blob/master/examples/verbal_expressions.py) using [pseudo-python](https://github.com/alehander42/pseudo-python)

That's a simple library similar to [VerbalExpressions](https://github.com/VerbalExpressions/PythonVerbalExpressions)

It defines a DSL for more readable definition of regular expressions and uses it with the example from [VerbalExpressions README](https://github.com/VerbalExpressions/PythonVerbalExpressions)

It demonstrates 

* suitabillity for writing/porting little libraries and DSL-s

* native standard library use: Pseudo uses the target language
standard library string/regex methods/functions

* oop handling: It uses prototypical oop in the js version and class-based code in the other versions

* string interpolation: pseudo-python recognizes and even checks the types of c-style `%d%s` formatting strings and it uses an idiomatic interpolation mechanism for each of the target languages

 
Commands: (assuming you're in `examples/verbal_expressions`)

* python

	translate to py with
    ```bash
    # from python source
    > pseudo-python original.py verbal_expressions.py
    #or from ast
    > pseudo verbal_expressions.pseudo.yaml py
    ```


    and run with
    ```
    > python verbal_expressions.py
    ```

* javascript
	
	translate to js with
    ```bash
    # from python source
    > pseudo-python original.py verbal_expressions.js
    #or from ast
    > pseudo verbal_expressions.pseudo.yaml js
    ```

    and run with
    ```bash
    > node verbal_expressions.js
    ```

* ruby

	translate to ruby with

    ```bash
    # from python source
    > pseudo-python original.py verbal_expressions.rb
    #or from ast
    > pseudo verbal_expressions.pseudo.yaml rb
    ```

    and run with
    ```bash
    > ruby verbal_expressions.rb
    ```

* c#
    
    translate to c# with

    ```bash
    # from python source
    > pseudo-python original.py verbal_expressions.cs
    #or from ast
    > pseudo verbal_expressions.pseudo.yaml csharp
    ```

    and run with
    ```bash
    > mcs verball_expressions.cs # or an equivalent command compiling cs files
    > ./verbal_expressions.exe
    ```

