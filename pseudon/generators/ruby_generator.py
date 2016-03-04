from pseudon.code_generator import CodeGenerator, switch
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

    def ruby_dict(self, node, indent):
        short_syntax = True
        result = []
        for pair in node.pairs:
            if short_syntax and pair.key.type == 'String' and re.match(SHORT_SYNTAX, pair.key.value):
                result.append('%s: %s' % (pair.key.value, self._generate_node(pair.value)))
            else:
                short_syntax = False
                result.append('%s => %s' % (self._generate_node(pair.key), self._generate_node(pair.value)))
        return ', '.join(result)

    def index_sequence(self, node, indent):
        h = self._generate_node(node.sequence)
        if node.sequence.pseudon_type.startswith('List'):
            return '%s.each_with_index' % h
        elif node.sequence.pseudon_type.startswith('Dictionary'):
            return '%s.each' % h
        elif node.sequence.pseudon_type == 'String':
            return '%s.each_char.each_with_index' % h
        else:
            return '%s.each' % h

    def index_iterator(self, node, indent):
        index, iterator = self._generate_node(node.index), self._generate_node(node.iterator)
        if node.sequence.pseudon_type.startswith('List'):
            return '%s, %s' % (iterator, index)
        elif node.sequence.pseudon_type.startswith('Dictionary'):
            return '%s, %s' % (index, iterator)
        elif node.sequence.pseudon_type == 'String': # we want to have explicitly all cases
            return '%s, %s' % (iterator, index)
        else:
            return '%s, %s' % (iterator, index)

    def each(self, node, indent):
        if node.sequence.pseudon_type.startswith('List') or node.sequence.pseudon_type.startswith('Dictionary'):
            return 'each'
        elif node.sequence.pseudon_type == 'String':
            return 'each_char'
        else:
            return 'each'

    call_args = ("(%<args:join ', '>)", '')
    function_params = ("(%<params:join ', '>)", '')

    templates = dict(
        module         = '%<dependencies:lines>%<definitions:lines>%<main:lines>',

        function_definition = '''
            def %<name>%<.params>
              %<block:lines>
            end''',

        function_definition_params = function_params,

        method_definition =     '''
            def %<name>%<.params>
              %<block:lines>
            end''',

        method_definition_params = function_params,

        constructor = '''
            def initialize%<.params>
              %<block:lines>
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

        list            = "[%<elements:join ', '>]",
        dictionary      = '{%<#ruby_dict>}',
        attr            = '%<object>.%<attr>',
        attr_assignment = '%<attr> = %<value>',
        local_assignment = '%<local> = %<value>',
        instance_assignment = '@%<name> = %<value>',

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>%<.args>",
        static_call_args = call_args,
        call        = switch(
            lambda c: c.function.name if c.function.type == 'local' else '',

            puts       = "puts %<args:join ', '>",
            _otherwise = "%<function>%<.args>"
        ),
        call_args   = call_args,
        method_call = "%<receiver>.%<message>%<.args>",
        method_call_args = call_args,

        this            = 'self',

        instance_variable = '@%<name>',

        throw_statement = 'throw %<exception>.new(%<value>)',

        if_statement    = '''
            if %<test>
              %<block:line_join>
            %<.otherwise>
            end''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            elsif %<test>
              %<block:line_join>
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else
              %<block:line_join>''',

        while_statement = '''
            while %<test>
              %<block:line_join>
            end''',

        try_statement = '''
            begin
              %<block:line_join>
            %<handlers:lines>
            end''',

        exception_handler = '''
            rescue %<.is_builtin> => %<instance>
              %<block:line_join>''',

        exception_handler_is_builtin = ('StandardError', '%<exception>'),

        for_each_statement = '''
            %<sequence>.%<#each> do |%<iterator>|
              %<block:line_join>
            end''',

        for_range_statement = '''
            (%<.first>...%<last>)%<.step>.each do |%<index>|
              %<block:lines>
            end''',

        for_range_statement_first = ('%<first>, ', '0'),

        for_range_statement_step = ('.step(%<step>)', ''),

        for_each_with_index_statement = '''
            %<#index_sequence> do |%<#index_iterator>|
              %<block:line_join>
            end''',

        explicit_return = 'return %<value>',

        implicit_return = '%<value>',

        custom_exception = '''
            class %<name> < %<.base>
            end''',

        custom_exception_base = ('%<base>', 'StandardError'),

        _slice          = '[%<from_>...%<to>]',
        _slice_from     = '[%<from_>..-1]',

        anonymous_function = '-> %<.params> %<anon_block>',

        anonymous_function_params = function_params,

        index           = '%<sequence>[%<index>]',

        index_assignment = '%<sequence>[%<index>] = %<value>',

        block           = '%<block:line_join>'
    )
