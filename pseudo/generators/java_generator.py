from pseudo.code_generator import CodeGenerator


class JavaGenerator(CodeGenerator):
    '''Java generator'''

    templates = {
        'program': '%<code>',
        'function': '''
                    public %{return_type} %<name>(%<args:join ','> {
                      %<body>
                    }
                    '''
    }
