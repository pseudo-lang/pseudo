'''
Pseudo: a library for idiomatic code generation

Pseudo is a library for generating code 
in different high level languages
and a system for language translation: 
its goal is to be able to translate any code expressed in a 
certain "pseudo-translateable" subset of each supported language
or as a pseudo AST to readable and idiomatic code in any of 
the supported target languages. 

Supported target languages currently are 
Python, Ruby, C#, JavaScript, Go
Soon: C++, Java, Nim
'''

import pseudo.api_translators
import pseudo.api_translators.ruby_translator
import pseudo.api_translators.python_translator
import pseudo.api_translators.js_translator
import pseudo.api_translators.csharp_translator
import pseudo.api_translators.cpp_translator
import pseudo.api_translators.golang_translator

import pseudo.generators
import pseudo.generators.ruby_generator
import pseudo.generators.python_generator
import pseudo.generators.js_generator
import pseudo.generators.csharp_generator
import pseudo.generators.cpp_generator
import pseudo.generators.golang_generator

import pseudo.loader
from pseudo.pseudo_tree import Node, to_node, call, method_call, attr, assignment, local

SUPPORTED_FORMATS = {'js', 'javascript', 'py', 'python', 'rb', 'ruby', 'go', 'golang', 'cs', 'csharp', 'cpp'}
FILE_EXTENSIONS = {'js': 'js', 'javascript': 'js', 'py': 'py', 'python': 'py', 'rb': 'rb', 'ruby': 'rb', 'go': 'go', 'golang': 'go', 'cs': 'cs', 'csharp': 'cs', 'cpp': 'cpp'}
FULL_NAMES = {'js': 'javascript', 'javascript': 'javascript', 'py': 'python', 'python': 'python', 'rb': 'ruby', 'ruby': 'ruby', 'csharp': 'c#', 'cs': 'c#', 'go': 'golang', 'golang': 'golang', 'cpp': 'c++'}
NAMES = {'js': 'JS', 'javascript': 'JS', 'py': 'Python', 'python': 'Python', 'rb': 'Ruby', 'ruby': 'Ruby', 'c#': 'CSharp', 'cs': 'CSharp', 'csharp': 'CSharp', 'golang': 'Golang', 'go': 'Golang', 'cpp': 'Cpp'}

API_TRANSLATORS = {
    format: getattr(
                getattr(
                    pseudo.api_translators,
                    '%s_translator' % NAMES[format].lower()),
                '%sTranslator' % NAMES[format])
    for format in SUPPORTED_FORMATS
}

GENERATORS = {
    format: getattr(
                getattr(
                    pseudo.generators,
                    '%s_generator' % NAMES[format].lower()),
                '%sGenerator' % NAMES[format])
    for format in SUPPORTED_FORMATS
}
        
def generate_main(main, language):
    '''
    generate output code for main in `language`

    `main` is a dict/Node or a list of dicts/Nodes with pseudo ast

    e.g.
    > print(generate_main({'type': 'int', 'value': 0, 'pseudo_type': 'Int'}, 'rb'))
    2
    > print(generate_main([pseudo.pseudo_tree.to_node('a'), pseudo.pseudo_tree.to_node(0)], 'js'))
    'a';
    0;
    '''
    base = {'type': 'module', 'custom_exceptions': [], 'definitions': [], 'constants': [], 'main': [], 'pseudo_type': 'Void'}
    base_node = pseudo.loader.convert_to_syntax_tree(base)
    if isinstance(main, dict):
        base['main'] = [main]
    elif isinstance(main, list):
        if main and isinstance(main[0], dict):
            base['main'] = main
        else:
            base_node.main = main
    elif isinstance(main, pseudo.pseudo_tree.Node):
        base_node.main = [main]
    if base['main']:
        q = pseudo.loader.convert_to_syntax_tree(base)
    else:
        q = base_node
    return generate(q, language)

def generate_from_yaml(pseudo_ast, language):
    '''
    generate output code in `language`

    converts yaml input to a Node-based pseudo internal tree and
    passes it to `generate

    '''
    return pseudo.generate(pseudo.loader.as_tree(pseudo_ast), language)


def generate(pseudo_ast, language):
    '''
    generate output code in `language`

    `pseudo_ast` can be a plain `dict` with ast data or
    it can use the internal `pseudo` `Node(type, **fields)` format

    if you want to play with it, you can use `generate_main` which 
    expects just a dict node / a list of dict nodes and a language

    `language` can be 'py', 'python', 'rb', 'ruby',
      'javascript', 'js', 'cs', 'csharp', 'go' or 'cpp'
    '''

    if isinstance(pseudo_ast, dict):
        pseudo_ast = pseudo.loader.convert_to_syntax_tree(pseudo_ast)
    translated_ast = API_TRANSLATORS[language](pseudo_ast).api_translate()
    return GENERATORS[language]().generate(translated_ast)
