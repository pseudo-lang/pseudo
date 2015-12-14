from pseudon.code_generator import CodeGenerator, join, indent, eventually


class PythonGenerator(CodeGenerator):

    templates = {
        'program': join('%{code}', '\n'),
        'function': ['def %{name}(', join('args', ','), '):\n',
                     indent('body', 1), '\n'],
        'class': ['class %{name}:', eventually('parent', '(%{parent})'), ':\n',
                  indent('methods', 1), '\n'],
        'name': '%{label}',
        'int': '%{value}'
    }
