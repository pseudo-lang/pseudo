from pseudon.code_generator import CodeGenerator


class GolangGenerator(CodeGenerator):
    '''Go generator'''

    indent = 1
    use_spaces = False

    templates = {
        'program': '%<code>',
        'function': '''
                    func %<name>() {\n
                        %<body>
                    }
                    '''
    }
