from pseudon.code_generator import CodeGenerator, join, indent, eventually


class JSGenerator(CodeGenerator):

    templates = {
        'program': join('%{code}', '\n'),
        'function': ['function %{name}(', join('args', ','), '){\n',
                     indent('body', 1), '\n}\n'],
    }
