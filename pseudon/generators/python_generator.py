from pseudon.code_generator import CodeGenerator, indented


class PythonGenerator(CodeGenerator):
    '''Python code generator'''

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

    templates = {
        'module': "%<code>",

        'function': indented('''
                    def %<name>(%<args:join ','>):
                        %<#body>
                    '''),

        'class':  indented('''
                  class %<name>%?<(%<parent>)>:
                      %<#methods>
                  '''),

        'name': '%<label>',
        'int': '%<value>'
    }
