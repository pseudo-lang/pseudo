from pseudo.code_generator import CodeGenerator, switch
import re

SHORT_SYNTAX = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')

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

class RubyGenerator(CodeGenerator):
    '''Ruby code generator'''

    indent = 2
    use_spaces = True
    middlewares = []

    def ruby_dict(self, node, indent):
        short_syntax = True
        result = []
        for pair in node.pairs:
            if short_syntax and pair.key.type == 'string' and re.match(SHORT_SYNTAX, pair.key.value):
                result.append('%s: %s' % (pair.key.value, self._generate_node(pair.value)))
            else:
                short_syntax = False
                result.append('%s => %s' % (self._generate_node(pair.key), self._generate_node(pair.value)))
        return ', '.join(result)

    call_args = ("(%<args:join ', '>)", '')
    function_params = ("(%<params:join ', '>)", '')

    templates = dict(
        module         = '''
            %<dependencies:lines>
            %<custom_exceptions:lines>
            %<definitions:lines>
            %<main:lines>''',

        function_definition = '''
            def %<name>%<.params>
              %<block:line_join>
            end''',

        function_definition_params = function_params,

        method_definition =     '''
            def %<name>%<.params>
              %<block:line_join>
            end''',

        method_definition_params = function_params,

        constructor = '''
            def initialize%<.params>
              %<block:line_join>
            end''',

        constructor_params = function_params,

        class_definition     = '''
            class %<name>%<.base>
              %<methods:lines>
            end''',

        class_definition_base = ('< %<base>', ''),

        local           = '%<name>',
        typename        = '%<name>',
        int             = '%<value>',
        float           = '%<value>',
        string          = '%<#safe_single>',
        boolean         = '%<value>',
        null            = 'nil',

        dependency      = "require '%<name>'",

        list            = "[%<elements:join ', '>]",
        dictionary      = '{%<#ruby_dict>}',
        attr            = '%<object>.%<attr>',
        
        assignment = '%<target> = %<value>',

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>%<.args>",
        static_call_args = call_args,
        call        = switch(
            lambda c: c.function.type == 'local' and c.function.name == 'puts' or len(c.args) == 0,

            true       = "%<function>%<args:join_lws ', '>",
            _otherwise = "%<function>(%<args:join ', '>)"
        ),
        call_args   = call_args,
        method_call = "%<receiver>.%<message>%<.args>",
        method_call_args = call_args,

        this            = 'self',

        instance_variable = '@%<name>',

        throw_statement = 'throw %<exception>.new(%<value>)',

        new_instance    = "%<class_name>.new(%<args:join ', '>)",

        if_statement    = '''
            if %<test>
              %<block:line_join>
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', 'end'),

        elseif_statement = '''
            elsif %<test>
              %<block:line_join>
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', 'end'),

        else_statement = '''
            else
              %<block:line_join>
            end''',

        while_statement = '''
            while %<test>
              %<block:line_join>
            end''',

        try_statement = '''
            begin
              %<block:line_join>
            %<handlers:line_join>end
            ''',

        exception_handler = '''
            rescue %<.is_builtin> => %<instance>
              %<block:line_join>''',

        exception_handler_is_builtin = ('StandardError', '%<exception>'),

        for_statement = '''
            %<sequences> do |%<iterators>|
              %<block:line_join>
            end''',

        for_range_statement = '''
            (%<.first>...%<last>)%<.step>.each do |%<index>|
              %<block:line_join>
            end''',

        for_range_statement_first = ('%<first>', '0'),

        for_range_statement_step = ('.step(%<step>)', ''),

        for_each_with_index_statement = '''
            %<#index_sequence> do |%<#index_iterator>|
              %<block:line_join>
            end''',

        for_sequence = '%<sequence>.each',

        for_sequence_zip = "%<sequences:first>.zip(%<sequences:join_rest ', '>).each",

        for_sequence_with_index = '%<sequence>.each_with_index',

        for_sequence_with_items = '%<sequence>.each',

        for_iterator = '%<iterator>',

        for_iterator_zip = "%<iterators:join ', '>",

        for_iterator_with_index = '%<iterator>, %<index>',

        for_iterator_with_items = '%<key>, %<value>',

        explicit_return = 'return %<value>',

        implicit_return = '%<value>',

        custom_exception = '''
            class %<name> < %<.base>
            end''',

        custom_exception_base = ('%<base>', 'StandardError'),

        _rb_slice          = '%<sequence>[%<from_>...%<to>]',
        _rb_slice_from     = '%<sequence>[%<from_>..-1]',
        _rb_slice_to       = '%<sequence>[0..%<to>]',

        anonymous_function = switch(
            lambda a: len(a.block) == 1,
            true         = "->%<params:join_lws ', '> { %<block:join ''> }",
            _otherwise   = '''
                            ->%<params:join_lws ', '> do
                              %<block:line_join>
                            end'''
        ),

        index           = '%<sequence>[%<index>]',

        tuple    = "[%<elements:join ', '>]",

        array    = "[%<elements:join ', '>]",

        set      = "Set.new([%<elements:join ', '>])",

        regex    = "/%<value>/",

        block           = '%<block:line_join>'
    )
