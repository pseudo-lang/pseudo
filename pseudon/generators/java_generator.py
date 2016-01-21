from pseudon.code_generator import CodeGenerator, indented


class JavaGenerator(CodeGenerator):
    '''Java generator'''

    templates = {
        'program': '%<code>',
        'function': indented('''
                    public %{return_type} %<name>(%<args:join ','> {
                      %<body>
                    }
                    ''')
    }
