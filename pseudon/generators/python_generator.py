from pseudon.code_generator import CodeGenerator


EXPRESSION_TYPES = ['call', 'implicit_return']

class PythonGenerator(CodeGenerator):
    '''Python code generator'''

    indent = 4
    use_spaces = True

    def to_boolean(self, node, indent):
        if node.value == 'true':
            return 'True'
        else:
            return 'False'

    def block(self, node, indent):
        if node.block:
            e = self._generate_node(node.block[0])
            other = [self.offset(indent) + self._generate_node(n, indent) for n in node.block[1:]]
            return '\n'.join([e] + other)
        else:
            return 'pass'

    def anonymous_function(self, node, indent):
        params = ', '.join(map(self._generate_node, node.params))
        lambda_head = 'lambda%s:' % (' ' + params if params else '')
        if not node.block:
            return '%s pass' % lambda_head
        elif len(node.block) == 1 and node.block[0].type in EXPRESSION_TYPES:
            if node.block[0].type == 'implicit_return' or node.block[0].type == 'explicit_return':
                block = node.block[0].value
            else:
                block = node.block[0]
            return '%s %s' % (lambda_head, self._generate_node(block))
        else:
            name = 'a_%d' % len(self.a)
            block = [self.offset(1) + self._generate_node(z) for z in node.block]
            code = 'def %s(%s):\n%s\n' % (name, params, '\n'.join(block))
            self.a.append(code)
            return name

    def index_sequence(self, node, indent):
        if node.sequence.pseudo_type.startswith('List'):
            return 'enumerate(%s)' % self._generate_node(node.sequence)
        else:
            return '%s.items()' % self._generate_node(node.sequence)

    templates = dict(
        module     = "%<dependencies:lines>%<constants:lines>%<definitions:lines>%<main:lines>",

        function_definition   = '''
             def %<name>(%<params:join ','>):
                 %<#block>''',

        function_definition_block = ("%<block:line_join>", 'pass'),

        method_definition =     '''
            def %<name>(self%<params:each_lpad ', '>):
                %<#block>''',

        method_definition_block = ('%<block:line_join>', 'pass'),

        class_definition = '''
              class %<name>%<.base>:
                  %<.constructor>
                  %<.methods>''',

        class_definition_methods = ("%<methods:line_join>", 'pass'),

        class_definition_base = ('(%<base>)', ''),

        class_definition_constructor = ('%<constructor>', ''),

        anonymous_function = '%<#anonymous_function>',

        constructor = '''
            def __init__(self%<.params>):
                %<#block>''',

        constructor_params = ("%<params:each_lpad ', '>", ''),

        dependency  = 'import %<name>',


        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_single>',
        boolean     = '%<#to_boolean>',
        null        = 'None',

        list        = "[%<elements:join ', '>]",
        dictionary  = "{%<pairs:join ', '>}",
        pair        = "%<key>: %<value>",
        attr        = "%<object>.%<attr>",

        local_assignment    = '%<local> = %<value>',
        instance_assignment = 'self.%<name> = %<value>',
        attr_assignment     = '%<attr> = %<value>',

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        _del        = 'del %<value>',
        _setitem    = '%<sequence>[%<key>] = %<value>',
        _slice      = '%<sequence>[%<from_>:%<to>]',
        _slice_from = '%<sequence>[%<from_>:]',
        _slice_to   = '%<sequence>[:%<to>]',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",

        block       = '%<block:lines>',

        this        = 'self',

        instance_variable = 'self.%<name>',

        throw_statement = 'throw %<exception>(%<value>)',

        if_statement    = '''
            if %<test>:
                %<#block>
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            elif %<test>:
                %<#block>
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else:
                %<#block>''',

        while_statement = '''
            while %<test>:
                %<#block>''',

        try_statement = '''
            try:
                %<#block>
            %<handlers:lines>''',

        exception_handler = '''
            except %<exception> as %<instance>:
                %<#block>''',

        for_each_statement = '''
            for %<iterator> in %<sequence>:
                %<#block>''',
    
        for_range_statement = '''
            for %<index> in range(%<.first>%<last>%<.step>):
                %<#block>''',

        for_range_statement_first = ('%<first>, ', ''), 

        for_range_statement_step = (', %<step>', ''),

        for_each_with_index_statement = '''
            for %<index>, %<iterator> in %<.sequence>:
                %<#block>''',

        for_each_with_index_statement_sequence = ('%<#index_sequence>', ''),

        for_each_in_zip_statement = '''
            for %<iterators:join ', '> in zip(%<sequences:join ', '>):
                %<#block>''',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        _with = '''
            with %<call> as %<context>:
                %<#block>''',

        custom_exception = '''
            class %<name>(%<.base>):
                pass''',

        custom_exception_base = ('%<base>', 'Exception'),

        constant = '%<constant> = %<init>',

        index    = '%<sequence>[%<index>]',

        index_assignment = '%<sequence>[%<index>] = %<value>'
    )
