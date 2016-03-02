from pseudon.code_generator import CodeGenerator


class CSharpGenerator(CodeGenerator):
    '''CSharp code generator'''

    indent = 4
    use_spaces = True

    def params(self, node, indent):
        return ', '.join(
            '%s %s' % (
              self.render_type(node.pseudo_type[:-1].partition('[')[2].split(', ')[j]), 
              k) for j, k in enumerate(node.params) )

    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': 'List<{0}>',
      'Dictionary': 'Dictionary<{0}, {1}>',
      'Void': 'void'
    }

    templates = dict(
        module     = '''
          %<dependencies:lines>public class Program
          {
              %<constants:lines>
              %<definitions:lines>
              public static void Main()
              {
                  %<main:semi>
              }
          }''',

        function_definition   = '''
            static %<@return_type> %<name>(%<#params>)
            {
                %<block:semi>
            }''',

        method_definition =     '''
            %<@return_type> %<name>(%<#params>)
            {
                %<block:semi>}''',

        class_definition = '''
              public class %<name>%<.base>
              {
                %<.constructor>
                %<methods:lines>}''',

        class_definition_base = (': %<base>', ''),

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
