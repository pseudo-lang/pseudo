from pseudon.code_generator import CodeGenerator, join, indent, eventually


class PHPGenerator(CodeGenerator):

    templates = {
        'program': ['<?php\n', join('%{code}', '\n')],
        'function': ['function %{name}(', join('args', ','), ') {\n', indent('body', 1, ';'), '%{indent}}\n'],
        'class': ['class %{name}', eventually('parent', ' extends %{parent}'), ' {\n', indent('methods', 1), '%{indent}}\n'],
        'name': '$%{label}',
        'int': '%{value}'
    }
