from pseudo.code_generator import CodeGenerator, switch


EXPRESSION_TYPES = ['call', 'implicit_return', 'method_call', 'explicit_return', 'binary_op', 'int', 'float', 'local']
    
class PythonGenerator(CodeGenerator):
    '''Python code generator'''

    indent = 4
    use_spaces = True
    middlewares = []

    templates = dict(
        module     = '''
            %<dependencies:lines>
            %<constants:lines>
            %<custom_exceptions:lines>
            %<definitions:lines>
            %<main:lines>''',

        function_definition   = '''
             def %<name>(%<params:join ', '>):
                 %<block:line_join_pass>''',

        function_definition_block = ("%<block:line_join>", 'pass'),

        method_definition =     '''
            def %<name>(self%<params:each_lpad ', '>):
                %<block:line_join_pass>''',

        method_definition_block = ('%<block:line_join>', 'pass'),

        class_definition = '''
              class %<name>%<.base>:
                  %<.constructor>
                  %<methods:line_join>
                  %<#class_pass>''',

        class_definition_base = ('(%<base>)', ''),

        class_definition_constructor = ('%<constructor>', ''),

        new_instance = "%<class_name>(%<args:join ', '>)",

        anonymous_function = '%<#anonymous_function>',

        constructor = '''
            def __init__(self%<.params>):
                %<block:line_join_pass>''',

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

        assignment    = '%<target> = %<value>',

        operation_assign    = '%<slot> %<op>= %<value>',

        binary_op   = '%<#binary_left> %<op> %<#binary_right>',
        
        unary_op    = switch(lambda u: u.op == 'not',
            true       = 'not %<value>',
            _otherwise = '%<op>%<value>'
        ),

        comparison  = '%<#binary_left> %<op> %<#binary_right>',

        _py_del        = 'del %<value>',
        _py_setitem    = '%<sequence>[%<key>] = %<value>',
        _py_slice      = '%<sequence>[%<from_>:%<to>]',
        _py_slice_from = '%<sequence>[%<from_>:]',
        _py_slice_to   = '%<sequence>[:%<to>]',


        static_call = switch(lambda s: len(s.args) == 1 and s.args[0].type == '_py_generatorcomp',
                true       = '%<receiver>.%<message>%<args:first>',
                _otherwise = "%<receiver>.%<message>(%<args:join ', '>)"),

        call        = switch(lambda s: len(s.args) == 1 and s.args[0].type == '_py_generatorcomp',
                true       = '%<function>%<args:first>',
                _otherwise = "%<function>(%<args:join ', '>)"),

        method_call = switch(lambda s: len(s.args) == 1 and s.args[0].type == '_py_generatorcomp',
                true       = '%<receiver>.%<message>%<args:first>',
                _otherwise = "%<receiver>.%<message>(%<args:join ', '>)"),
        
        this_method_call = switch(lambda s: len(s.args) == 1 and s.args[0].type == '_py_generatorcomp',
                true       = 'self.%<message>%<args:first>',
                _otherwise = "self.%<message>(%<args:join ', '>)"),

        block       = '%<block:lines>',

        this        = 'self',

        instance_variable = 'self.%<name>',

        throw_statement = 'raise %<exception>(%<value>)',

        if_statement    = '''
            if %<test>:
                %<block:line_join_pass>
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            elif %<test>:
                %<block:line_join_pass>
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else:
                %<block:line_join_pass>''',

        while_statement = '''
            while %<test>:
                %<block:line_join_pass>''',

        try_statement = '''
            try:
                %<block:line_join_pass>
            %<handlers:lines>''',

        exception_handler = '''
            except %<.is_builtin> as %<instance>:
                %<block:line_join_pass>''',

        exception_handler_is_builtin = ('Exception', '%<exception>'),

        for_statement = '''
            for %<iterators> in %<sequences>:
                %<block:line_join_pass>''',
    
        for_range_statement = '''
            for %<index> in range(%<.first>%<end>%<.step>):
                %<block:line_join_pass>''',

        for_range_statement_first = ('%<start>, ', '%<start>, '), 

        for_range_statement_step = (', %<step>', ''),

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        _py_with = '''
            with %<call> as %<context>:
                %<block:line_join_pass>''',

        custom_exception = '''
            class %<name>(%<.base>):
                pass''',

        custom_exception_base = ('%<base>', 'Exception'),

        constant = '%<constant> = %<init>',

        # standard_iterable_call = switch('function',
        #     map = '[%<.block>]',
        #     filter_map = "[%<.block> if %<test:join ''>]",
        #     _otherwise = '%<function>([%<.block>])'
        # ),

        # standard_iterable_call_range = "[%<block:join ''> for %<index> in range(%<.first>%<last>%<.step>)]",

        # standard_iterable_call_block = ("%<block:join ''> for %<iterators> in %<sequences>", ''),

        # standard_iterable_call_first = ('%<first>, ', ''), 

        # standard_iterable_call_step = (', %<step>', ''),
        
        for_iterator = '%<iterator>',

        for_iterator_zip = "%<iterators:join ', '>",

        for_iterator_with_index = '%<index>, %<iterator>',

        for_iterator_with_items = '%<key>, %<value>',

        for_sequence = '%<sequence>',

        for_sequence_zip = "zip(%<sequences:join ', '>)",

        for_sequence_with_index = 'enumerate(%<sequence>)',

        for_sequence_with_items = '%<sequence>.items()',

        tuple    = "(%<elements:join ', '>)",

        array    = "(%<elements:join ', '>)",

        set      = '%<.elements>',

        set_elements = (
            "{%<elements:join ', '>}",
            'set()'
        ),

        index    = '%<sequence>[%<index>]',

        interpolation = "'%<args:join ''>'.format(%<#placeholders>)",

        interpolation_literal = '%<value>',

        break_ = 'break',

        interpolation_placeholder = '{%<index>}',

        _py_listcomp = '[%<block> for %<iterators> in %<sequences>%<#test>]',

        _py_generatorcomp = '(%<block> for %<iterators> in %<sequences>%<#test>)',

        _py_in   = '%<value> in %<sequence>',

        _py_step = '%<sequence>[::%<step>]',

        not_null_check = '%<value> is not None',

        aug_assignment = '%<target> %<op>= %<value>',

        standard_iterable_call = '[%<block:first> for %<iterators> in %<sequences> if %<test:first>]',

        regex    = "re.compile(r'%<value>')",

    )
    
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

    def class_pass(self, node, indent):
        if not node.constructor and not node.methods:
            return 'pass'
        else:
            return ''

    def test(self, node, indent):
        if node.test:
            return ' if %s' % self._generate_node(node.test)
        else:
            return ''

    def placeholders(self, node, indent):
        return ', '.join(self._generate_node(placeholder.value) for placeholder in node.args[1::2])