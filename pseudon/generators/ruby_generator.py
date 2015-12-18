from pseudon.code_generator import CodeGenerator, indented


class RubyGenerator(CodeGenerator):
    '''Ruby code generator'''

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

        'name': '%<label>',
        'int': '%<value>'
    }
