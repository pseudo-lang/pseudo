'''pseudon is translating asts'''
import pseudon.api_translators.ruby_translator
import pseudon.api_translators.python_translator
import pseudon.api_translators.js_translator
import pseudon.api_translators.java_translator
import pseudon.api_translators.csharp_translator
import pseudon.api_translators.cpp_translator
# import pseudon.api_translators.go_translator

import pseudon.generators.ruby_generator
import pseudon.generators.python_generator
import pseudon.generators.js_generator
import pseudon.generators.java_generator
import pseudon.generators.csharp_generator
import pseudon.generators.cpp_generator
# import pseudon.generators.go_generator


SUPPORTED_FORMATS = {'js', 'javascript', 'py', 'python', 'rb', 'ruby', 'php', 'java'}
FILE_EXTENSIONS = {'js': 'js', 'javascript': 'js', 'py': 'py', 'python': 'py', 'rb': 'rb', 'ruby': 'rb', 'php': 'php', 'java': 'java'}
FULL_NAMES = {'js': 'javascript', 'javascript': 'javascript', 'py': 'python', 'python': 'python', 'rb': 'ruby', 'ruby': 'ruby', 'csharp': 'c#', 'cs': 'c#', 'java': 'java', 'cpp': 'c++'}
NAMES = {'js': 'JS', 'javascript': 'JS', 'py': 'Python', 'python': 'Python', 'rb': 'Ruby', 'ruby': 'Ruby', 'c#': 'CSharp', 'cpp': 'Cpp'}

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
    translated_ast = API_TRANSLATORS[language](pseudon_ast).api_translate()
    return GENERATORS[language].generate(translated_ast)
