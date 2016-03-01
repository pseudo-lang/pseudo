from pseudon.code_generator import CodeGenerator


class PHPGenerator(CodeGenerator):
    '''PHP code generator'''

    def body(self, node, indent):
        if node.body:
            return self.render_nodes(node.body, indent)
        else:
            return '%spass\n' % self.offset(indent)

    def methods(self, node, indent):
        if node.methods:
            return self.render_nodes(node.methods, indent)
        else:
            return '%spass\n' % self.offset(indent)

    '''similar to dynamic ones'''
    templates = {
        'module': "<?php\n%<code>",

        'function': '''
                    function %<name>(%<args:join ','>) {
                        %<#body>
                    }
                    ''',

        'class':  '''
                  class %<name>%?<(%<parent>)>:
                      %<#methods>
                  ''',

        'name': '%<label>',
        'int': '%<value>'
    }
