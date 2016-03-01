from pseudon.code_generator import CodeGenerator


class RubyGenerator(CodeGenerator):
    '''Ruby code generator'''

    indent = 2
    use_spaces = True

    def lquote(self, node, indent):
        return '(' if node.args else ''

    def rquote(self, node, indent):
        return ')' if node.args else ''

    templates = {
        'module': "%<code>",

        'function': '''
                    def %<name>%<#lquote>%<args:join ', '>%<#rquote>
                      %<body>
                    end
                    ''',

        'class':  '''
                  class %<name>%?< < %<parent>>:
                    %<methods>
                  ''',

        'local': '%<name>',
        'int': '%<value>',
        'float': '%<value>',
        'string': '%<#safe_single>',
        'boolean': '%<value>',
        'null': 'nil'
    }
