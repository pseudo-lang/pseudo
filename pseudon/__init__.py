'''pseudon is translating asts'''
import pseudon.api_translators
import pseudon.api_translators.ruby_translator
import pseudon.api_translators.python_translator
import pseudon.api_translators.js_translator
import pseudon.api_translators.csharp_translator
import pseudon.api_translators.cpp_translator
import pseudon.api_translators.golang_translator
import pseudon.api_translators.php_translator

import pseudon.generators
import pseudon.generators.ruby_generator
import pseudon.generators.python_generator
import pseudon.generators.js_generator
import pseudon.generators.csharp_generator
import pseudon.generators.cpp_generator
import pseudon.generators.golang_generator
import pseudon.generators.php_generator

SUPPORTED_FORMATS = {'js', 'javascript', 'py', 'python', 'rb', 'ruby', 'php', 'go', 'golang'}
FILE_EXTENSIONS = {'js': 'js', 'javascript': 'js', 'py': 'py', 'python': 'py', 'rb': 'rb', 'ruby': 'rb', 'php': 'php', 'go': 'golang', 'golang': 'golang'}
FULL_NAMES = {'js': 'javascript', 'javascript': 'javascript', 'py': 'python', 'python': 'python', 'rb': 'ruby', 'ruby': 'ruby', 'csharp': 'c#', 'cs': 'c#', 'go': 'golang', 'golang': 'golang', 'cpp': 'c++', 'php': 'php'}
NAMES = {'js': 'JS', 'javascript': 'JS', 'py': 'Python', 'python': 'Python', 'rb': 'Ruby', 'ruby': 'Ruby', 'c#': 'CSharp', 'golang': 'Golang', 'go': 'Golang', 'cpp': 'Cpp', 'php': 'PHP'}

API_TRANSLATORS = {
    format: getattr(
                getattr(
                    pseudon.api_translators,
                    '%s_translator' % NAMES[format].lower()),
                '%sTranslator' % NAMES[format])
    for format in SUPPORTED_FORMATS
}

GENERATORS = {
    format: getattr(
                getattr(
                    pseudon.generators,
                    '%s_generator' % NAMES[format].lower()),
                '%sGenerator' % NAMES[format])
    for format in SUPPORTED_FORMATS
}


def generate(pseudon_ast, language):
    '''generate output code in the given language'''
    # print('PARSE', pseudon_ast.y)
    translated_ast = API_TRANSLATORS[language](pseudon_ast).api_translate()
    # print('AFTER', translated_ast.y)
    return GENERATORS[language]().generate(translated_ast)
