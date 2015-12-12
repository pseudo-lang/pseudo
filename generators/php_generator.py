from pseudon.code_generator import CodeGenerator


class PHPGenerator(CodeGenerator):

    templates = {
        'program': '%code~join<\n>~'
        'function': 'function %name(%args~join<,>) {\n' +
                    '%body~indent<1>~\n}\n'
    }
