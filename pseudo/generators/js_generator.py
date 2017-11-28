import re
from pseudo.code_generator import CodeGenerator, switch
from pseudo.middlewares import DeclarationMiddleware

JS_NAME = re.compile(r'[a-zA-Z][a-zA-Z_0-9]*')
OPS = {'not': '!', 'and': '&&', 'or': '||'}

def index_switch(i):
    if i.index.type == 'string' and JS_NAME.match(i.index.value):
        return 'string'
    elif i.index.type == 'int' and i.index.value < 0:
        return 'z'
    else:
        return 'normal'

class JSGenerator(CodeGenerator):
    '''JS generator'''

    indent = 2
    use_spaces = True
    middlewares = [DeclarationMiddleware]

    templates = dict(
        module     = "%<dependencies:lines>%<constants:lines>%<custom_exceptions:lines>%<definitions:lines>%<main:semi>",

        function_definition   = '''
            function %<name>(%<params:join ', '>) {
              %<block:semi>
            }''',

        method_definition =     '''
            %<this>.prototype.%<name> = function (%<params:join ', '>) {
              %<block:semi>
            }''',

        class_definition = '''
              %<.constructor>
              %<.base>
              %<methods:lines>''',

        class_definition_base = ('%<name>.prototype = _.create(%<base>.prototype, {constructor: %<name>})', ''),

        class_definition_constructor = ('%<constructor>', ''),

        dependency = switch('name',
            lodash = "var _ = require('%<name>');",
            _otherwise = "var %<name> = require('%<name>');"
        ),

        anonymous_function = '''
            function (%<params:join ', '>) {
              %<block:semi>
            }''',

        constructor = '''
            function %<this>(%<params:join ', '>) {
              %<block:semi>
            }''',

        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_single>',
        boolean     = '%<value>',
        null        = 'null',

        list        = "[%<elements:join ', '>]",
        dictionary  = "{%<pairs:join ', '>}",
        pair        = switch(lambda p: p.key.type == 'string' and JS_NAME.match(p.key.value) is not None,
                true = '%<key.value>: %<value>',
                _otherwise = '%<key>: %<value>'
        ),
        attr        = "%<object>.%<attr>",

        custom_exception = '''
            function %<name>(message) {
              this.message = message;
            }

            %<name>.prototype = _.create(%<.base>.prototype, {constructor: %<name>});''',        

        custom_exception_base = ('%<base>', 'Error'),

        assignment    = switch('first_mention',
            true = 'var %<target> = %<value>',
            _otherwise = '%<target> = %<value>'
        ),

        binary_op   = '%<#binary_left> %<#op> %<#binary_right>',
        unary_op    = '%<#op>%<value>',
        comparison  = '%<#comparison>',

        static_call = "%<receiver>.%<message>(%<#args_join>)",
        call        = "%<function>(%<#args_join>)",
        method_call = "%<receiver>.%<message>(%<#args_join>)",
        this_method_call = "this.%<message>(%<#args_join>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        throw_statement = 'throw new %<exception>(%<value>)',

        new_instance    = "new %<class_name>(%<args:join ', '>)",

        if_statement    = '''
            if (%<test>) {
              %<block:semi>
            } %<.otherwise>''',

        if_statement_otherwise = (' %<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>) {
              %<block:semi>
            } %<.otherwise>''',

        elseif_statement_otherwise = (' %<otherwise>', ''),

        else_statement = '''
            else {
              %<block:semi>
            }''',
            

        while_statement = '''
            while (%<test>) {
                %<block:semi>
            }''',

        try_statement = '''
            try {
              %<block:semi>
            } catch(%<#handler_>) {
              if %<handlers:join_depth_aware ' else if '> else {
                throw %<#handler_>;
              }
            }''',

        exception_handler = '''
            (%<instance> isinstanceof %<.is_builtin>) {
              %<block:semi>
            }''', # obvsly its an Error, but we'll have other builtin errors in next versions

        exception_handler_is_builtin = ('Error', '%<exception>'),

        for_statement = '''
            _.forEach(%<sequences>, function (%<iterators>) {
              %<block:semi>
            })''',

        for_range_statement = '''
            for(var %<index> = %<.first>;%<index> != %<end>;%<index> += %<.step>) {
              %<block:semi>
            }''',

        for_range_statement_first = ('%<start>', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_iterator = '%<iterator>',

        for_iterator_zip = "%<iterators:join ', '>",

        for_iterator_with_index = '%<iterator>, %<index>',

        for_iterator_with_items = '%<value>, %<key>',

        for_sequence = '%<sequence>',

        for_sequence_zip = "_.zip(%<sequences:join ', '>)",

        for_sequence_with_index = '%<sequence>',

        for_sequence_with_items = '%<sequence>',

        tuple = "[%<elements:join ', '>]",

        array = "[%<elements:join ', '>]",

        set   = "{%<.elements>}",

        set_elements = ("%<elements:join ': true, '>: true", ''),

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index = switch(
            index_switch,
              string       = '%<sequence>.%<index.value>',
              normal       = '%<sequence>[%<index>]',
              _otherwise   = '%<sequence>[%<sequence>.length - %<#index>]'
        ),

        interpolation = "%<args:join ' + '>",

        interpolation_literal = '%<#safe_single>',

        interpolation_placeholder = '%<value>',

        constant = '%<constant> = %<init>',

        aug_assignment = '%<target> += %<value>',

        standard_iterable_call = '''
            _.filter(%<sequences.sequence>, function (%<iterators>) {
              return %<test:first>;
            }).map(function (%<iterators>) {
              return %<block:first>;
            })''',

        block = '%<block:semi>',

        not_null_check = '%<value>',

        regex = '/%<value>/',
    )
    
    def handler_(self, node, indent):
        if node.handlers:
            return node.handlers[0].instance
        else:
            return '_e'
    def op(self, node, depth):
        return OPS.get(node.op, node.op)

    def args_join(self, node, depth):
        return ', '.join(
            self._generate_node(n, depth).lstrip() 
            for n
            in node.args)

    def comparison(self, node, depth):
        if node.left.type == 'binary_op' and node.left.op == '-' and node.left.right.type == 'int' and node.right.type == 'int':
            node.right.value += node.left.right.value
            node.left = node.left.left

        return '%s %s %s' % (self.binary_left(node, depth), node.op, self.binary_right(node, depth))

    def index(self, node, depth):
        return str(-node.index.value)
