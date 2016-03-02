from pseudon.code_generator import CodeGenerator


class JSGenerator(CodeGenerator):
    '''JS generator'''

    indent = 4
    use_spaces = True

    templates = dict(
        module     = "%<dependencies:lines>%<constants:lines>%<definitions:lines>%<main:semi>",

        function_definition   = '''
             function %<name>(%<params:join ','>) {
                 %<block:semi>}''',

        method_definition =     '''
            %<this>.prototype.%<name> = function(%<params:join ', '>) {
                %<block:semi>}''',

        class_definition = '''
              %<.constructor>
              %<.base>
              %<methods:lines>''',

        class_definition_base = ('%<name>.prototype = _.create(%<base>.prototype, {constructor: %<name>})', ''),

        class_definiton_constructor = ('%<constructor>', ''),

        anonymous_function = '''
            function (%<params:join ', '>) {
                %<block:semi>}''',

        constructor = '''
            function %<this>(%<params:join ', '>):
                %<block:semi>}''',

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
        pair        = "%<first>: %<second>",
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

        constant = '%<constant> = %<init>',

        block = '%<block:semi>'
    )
