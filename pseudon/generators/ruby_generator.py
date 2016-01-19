from pseudon.code_generator import CodeGenerator, join, indent, eventually


class RubyGenerator(CodeGenerator):
    '''Ruby code generator'''

    templates = {
        'program': join('code', '\n'),
        'function': ['def %{name}', eventually('args', '('),
                     join('args', ','), eventually('args', ')'), '\n',
                     indent('body', 1), '%{indent}end\n'],
        'class': ['class %{name}', eventually('parent', '< %{parent}'), '\n',
                  indent('methods', 1), '\n'],
        'name': '%{label}',
        'local': '%{name}',
        'int': '%{value}',
    }
