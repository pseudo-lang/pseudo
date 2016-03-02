from pseudon.code_generator import CodeGenerator
import re

SHORT_SYNTAX = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')

class RubyGenerator(CodeGenerator):
    '''Ruby code generator'''

    indent = 2
    use_spaces = True

    def ruby_dict(self, node, indent):
        short_syntax = True
        result = []
        for pair in node.pairts:
            if short_syntax and pair.first.type == 'String' and re.match(SHORT_SYNTAX, pair):
                result.append('%s: %s' % (pair.first.value, self._generate_node(pair.second, 0)))
            else:
                short_syntax = False
                result.append('%s => %s' % (self._generate_node(pair.first, 0), self._generate_node(pair.second, 0)))
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

    templates = dict(
        module         = '%<dependencies:lines>%<definitions:lines>%<main:lines>',

        function_definition = '''
            def %<name>%<.args>
              %<body:lines>
            end''',

        function_definition_args = ("(%<args:join ', '>)", ''),

        method_definition =     '''
            def %<name>%<.args>
              %<body:lines>
            end''',

        method_definition_args = ("(%<args:join ', '>", ''),

        class_definition     = '''
            class %<name>%<.parent>
              %<methods:lines>
            end''',

        class_definition_parent = ('< %<parent>', ''),

        local           = '%<name>',
        typename        = '%<name>',
        int             = '%<value>',
        float           = '%<value>',
        string          = '%<#safe_single>',
        boolean         = '%<value>',
        null            = 'nil',

        list            = "[%<elements:join ', '>]",
        dict            = '{%<#ruby_dict>}',
        attr            = '%<object>.%<attr>',
        attr_assignment = '%<attr> = %<value>',
        local_assignment = '%<local> = %<value>',
        instance_assignment = '@%<name> = %<value>',

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>%<.args>",
        static_call_args = call_args,
        call        = "%<function>%<.args>",
        call_args   = call_args,
        method_call = "%<receiver>.%<message>%<.args>",
        method_call_args = call_args,

        this            = 'self',

        instance_variable = '@%<name>',

        throw_statement = 'throw %<exception>.new(%<value>)',

        if_statement    = '''
            if %<test>
              %<block:line_join>
            %<.otherwise>end''',

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
              %<block:line_join>''',

        try_statement = '''
            begin
              %<block:line_join>
            %<handlers:lines>end''',

        exception_handler = '''
            rescue %<exception> => %<instance>
              %<block:line_join>''',

        for_each_statement = '''
            %<sequence>.%<#each> do |%<iterator>|
              %<block:line_join>end''',

        for_range_statement = '''
            (%<.first>...%<last>)%<.step>.each do |%<index>|
                %<block:lines>end''',

        for_range_statement_first = ('%<first>, ', '0'), 

        for_range_statement_step = ('.step(%<step>)', ''),

        for_each_with_index_statement = '''
            %<#index_sequence> do |%<#index_iterator>|
              %<block:line_join>end''',

        block           = '%<block:line_join>'
    )
