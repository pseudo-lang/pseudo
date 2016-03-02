from pseudon.code_generator import CodeGenerator


class JSGenerator(CodeGenerator):
    '''JS generator'''

    indent = 4
    use_spaces = True

    def index(self, node, depth):
        if node.index.type == 'String':
            return '.%s' % node.value
        else:
            return '[%s]' % self._generate_node(node.index)

    templates = dict(
        module     = "%<dependencies:lines>%<constants:lines>%<definitions:lines>%<main:semi>",

        function_definition   = '''
            function %<name>(%<params:join ','>) {
                %<block:semi>
            }''',

        method_definition =     '''
            %<this>.prototype.%<name> = function(%<params:join ', '>) {
               %<block:semi>
            }''',

        class_definition = '''
              %<.constructor>
              %<.base>
              %<methods:lines>''',

        class_definition_base = ('%<name>.prototype = _.create(%<base>.prototype, {constructor: %<name>})', ''),

        class_definiton_constructor = ('%<constructor>', ''),

        anonymous_function = '''
            function (%<params:join ', '>) {
                %<block:semi>
            }''',

        constructor = '''
            function %<this>(%<params:join ', '>):
                %<block:semi>
            }''',

        dependency  = "%<name> = require('%<name>');",


        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_single>',
        boolean     = '%<value>',
        null        = 'null',

        list        = "[%<elements:join ', '>]",
        dictionary  = "{%<pairs:join ', '>}",
        pair        = "%<key>: %<value>",
        attr        = "%<object>.%<attr>",

        local_assignment    = '%<local> = %<value>',
        instance_assignment = 'this.%<name> = %<value>',
        attr_assignment     = '%<attr> = %<value>',

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        _setitem    = '%<sequence>[%<key>] = %<value>',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        throw_statement = 'throw %<exception>(%<value>)',

        if_statement    = '''
            if (%<test>) {
                %<block:semi>
            }
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>) {:
                %<block:semi>
            }
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else {
                %<block:semi>
            }''',
            

        while_statement = '''
            while %<test> {
                %<block:semi>
            }''',

        try_statement = '''
            try {
                %<block:semi>
            }
            except(_e) {
              %<handlers:semi>
              raise e;
            }''',

        exception_handler = '''
            if (%<instance> isinstanceof %<exception>) {
                %<block:semi>
            }''',

        for_each_statement = '''
            _.each(%<sequence>, function(%<iterator>) {
                %<block:semi>
            })''',

        for_range_statement = '''
            for(var %<index> = %<.first>; %<index> != %<last>; %<index> += %<.step>) {
                %<block:semi>
            }''',

        for_range_statement_first = ('%<first>, ', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_each_with_index_statement = '''
            _.each(%<sequence>, function(%<iterator, %<index>) {
                %<block:semi>
            })''',

        for_each_in_zip_statement = '''
            _.zip(%<sequences:join ', '>).each(function(%<iterators:join ', '>) {
                %<#block>
            })''',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index = '%<sequence>%<#index>',

        index_assignment = '%<sequence>%<#index> = %<value>',

        constant = '%<constant> = %<init>',

        block = '%<block:semi>'
    )
