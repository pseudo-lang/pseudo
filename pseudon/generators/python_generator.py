from pseudon.code_generator import CodeGenerator, switch


EXPRESSION_TYPES = ['call', 'implicit_return', 'method_call', 'explicit_return']

PRIORITIES = {
    '**':   11,
    '%':    11,
    '/':    10,
    '*':    10,
    '+':    9,
    '-':    9,
    '>':    8,
    '<':    8,
    '>=':   8,
    '<=':   8,
    '==':   8,
    'and':  7,
    'or':   6,
}

    
class PythonGenerator(CodeGenerator):
    '''Python code generator'''

    indent = 4
    use_spaces = True
    middlewares = []

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

    def index_sequence(self, node, indent):
        if node.sequence.pseudo_type.startswith('List'):
            return 'enumerate(%s)' % self._generate_node(node.sequence)
        else:
            return '%s.items()' % self._generate_node(node.sequence)

    def binary_left(self, node, indent):
        return self.binary_side(node.left, node.op)

    def binary_right(self, node, indent):
        return self.binary_side(node.right, node.op)

    def binary_side(self, field, op):
        base = self._generate_node(field)
        print(field.pseudo_type)
        if (field.type == 'binary_op' or field.pseudo_type == 'comparison') and\
           PRIORITIES[field.op] < PRIORITIES[op]:
            return '(%s)' % base
        else:
            return base

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
                  %<methods:line_join>
                  %<#class_pass>''',

        class_definition_base = ('(%<base>)', ''),

        class_definition_constructor = ('%<constructor>', ''),

        new_instance = "%<class>(%<params:join ', '>)",

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

        assignment    = '%<target> = %<value>',

        operation_assign    = '%<slot> %<op>= %<value>',

        binary_op   = '%<#binary_left> %<op> %<#binary_right>',
        
        unary_op    = '%<op>%<value>',

        comparison  = '%<#binary_left> %<op> %<#binary_right>',

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

        this_method_call = "self.%<message>(%<args:join ', '>)",

        throw_statement = 'raise %<exception>(%<value>)',

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
            except %<.is_builtin> as %<instance>:
                %<#block>''',

        exception_handler_is_builtin = ('Exception', '%<exception>'),

        for_statement = '''
            for %<iterators> in %<sequences>:
                %<#block>''',
    
        for_range_statement = '''
            for %<index> in range(%<.first>%<last>%<.step>):
                %<#block>''',

        for_range_statement_first = ('%<first>, ', ''), 

        for_range_statement_step = (', %<step>', ''),

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

        standard_iterable_call = switch('function',
            map = '[%<.block>]',
            filter_map = "[%<.block> if %<test:join ''>]",
            _otherwise = '%<function>([%<.block>])'
        ),

        standard_iterable_call_range = "[%<block:join ''> for %<index> in range(%<.first>%<last>%<.step>)]",

        standard_iterable_call_block = ("%<block:join ''> for %<iterators> in %<sequences>", ''),

        standard_iterable_call_first = ('%<first>, ', ''), 

        standard_iterable_call_step = (', %<step>', ''),
        
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

        regex    = "re.compile(r'%<value>')",

        index    = '%<sequence>[%<index>]',
    )
