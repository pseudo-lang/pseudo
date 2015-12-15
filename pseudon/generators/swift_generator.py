from pseudon.code_generator import CodeGenerator, join, indent, eventually


class SwiftGenerator(CodeGenerator):

    templates = {
        'program': join('%{code}', '\n'),
        'function': ['def %{name}(', join('args', ','), '):\n',
                     indent('body', 1), '\n']
    }
