# extend pseudo 

## add support for a language as a target

The easiest way is:

  * Create tests (look at the other language tests and the 
  existing suite with inputs, you can very quickly bootstrap 
  a suite for your language)
  
  * Create a <Lang>Translator in `pseudo/api_translators`
    There are some DSL docs in `pseudo/api_translator.py`
    Again, other close target languages can be a good starting point 

  * For pseudo standard methods and functions that have a more 
    complicated equivalent in your target language, you need to 
    create a `<lang>_api_handlers.py` file and define functions and `Leaking Nodes`. Leaking nodes are classes defining the behavior of such complicated constructs in different contexts:
    mainly expression and assignment (that's how most of go equivalents or `with` in python are implemented)


  * Create a <LangGenerator> in `pseudo/generators`
    That's probably the most enjoyable part, for 15-20 minutes you can have the most of your target language syntax prepared


## compile a subset of a language to pseudo

  * Ping me.

  * (because I need to update and finish the pseudo ast documentation)

## add functions/methods/types to standard library

  * Add an example in `tests/suite.py`, try to look for the other methods/function from the same class/namespace

  * Add test outputs for each of the target languages 

  * Define a translation for the method/function in each corresponding api translator
