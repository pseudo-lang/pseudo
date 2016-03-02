from pseudon.code_generator import CodeGenerator


class PythonGenerator(CodeGenerator):
    '''Python code generator'''

    indent = 4
    use_spaces = True

    # def body(self, node, indent):
    #     if node.body:
    #         return self.render_nodes(node.body, indent)
    #     else:
    #         return '%spass\n' % self.offset(indent)

    # def methods(self, node, indent):
    #     if node.methods:
    #         return self.render_nodes(node.methods, indent)
    #     else:
    #         return '%spass\n' % self.offset(indent)

    def to_boolean(self, node, indent):
        if node.value == 'true':
            return 'True'
        else:
            return 'False'

    templates = dict(
        module     = "%<definitions:each_rpad '\\n'>%<main:each_rpad '\\n'>",

        function_definition   = '''
             def %<name>(%<params:join ','>):
                 %<.block>''',

        function_definition_block = ("%<block:join '\\n'>", 'pass'),

        class_definition = '''
              class %<name>%<.parent>:
                  %<.methods>''',

        class_definition_methods = ("%<methods:join '\\n'>", 'pass'),

        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_single>',
        boolean     = '%<#to_boolean>',
        null        = 'None',

        class_definition_parent = ('(%<parent>)', ''),

        local_assignment    = '%<local> = %<value>',
        instance_assignment = 'self.%<attr> = %<value>',
        attr_assignment     = '%<attr> = %<value>',

        _del        = 'del %<value>',
        _setitem    = '%<sequence>[%<key>] = %<value>',

        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>'
    )
