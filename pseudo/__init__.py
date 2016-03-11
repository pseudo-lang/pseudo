'''pseudo is translating asts'''
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


def generate(pseudo_ast, language):
    '''generate output code in the given language'''
    translated_ast = API_TRANSLATORS[language](pseudo_ast).api_translate()
    # print(language, API_TRANSLATORS[language].functions['io']['display'])
    # input()
    return GENERATORS[language]().generate(translated_ast)
