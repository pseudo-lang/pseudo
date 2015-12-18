from pseudon.code_generator import CodeGenerator, indented


class JSGenerator(CodeGenerator):
    '''JS generator'''

    templates = {
        'program': '%<code>',
        'function': '''
                    function %<name>(%<args:join ','>{
                      %<body>
                    }
                    '''
    }
