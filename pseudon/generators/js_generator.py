from pseudon.code_generator import CodeGenerator


class JSGenerator(CodeGenerator):
    '''JS generator'''

    templates = {
        'program': '%<code>',
        'function': '''
                    function %<name>(%<args:join ','>{
                      %<body>
                    }
                    ''',

        'local': '%<name>',
        'int':   '%<value>',
        'boolean': '%<value>',
        'null': 'null',

        'call': '%<function>(%<args:join ", ">)',
        'method_call': '%<receiver>.%<message>(%<args:join ", ">)',

        'return': 'return %<value>',
        'throw': 'throw new %<exception>(%<value>)'
    }	
