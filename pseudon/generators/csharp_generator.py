from pseudon.code_generator import CodeGenerator, switch
from pseudon.middlewares import DeclarationMiddleware

class CSharpGenerator(CodeGenerator):
    '''CSharp code generator'''

    indent = 4
    use_spaces = True
    middlewares = [DeclarationMiddleware]

    def params(self, node, indent):
        return ', '.join(
            '%s %s' % (
              self.render_type(node.pseudo_type[j + 1]), 
              self._generate_node(k)) for j, k in enumerate(node.params) )

    def anon_block(self, node, indent):
        if len(node.block) == 1:
            b = self._generate_node(node.block[0])
            return b
        else:
            b = ';\n'.join(self._generate_node(e, indent + 1) for e in node.block) + ';\n'
            return '{%s\n%s}' % (b, self.offset(indent))

    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': 'List<{0}>',
      'Dictionary': 'Dictionary<{0}, {1}>',
      'Set': 'Set<{0}>',
      'Tuple': lambda x: 'Tuple<{0}>'.format(', '.join(x)),
      'Array': '{0}[]', 
      # fixed-size buffers in c# are not widely used
      # they require a struct and an unsafe annotation
      # we can a unsafe-fixed-size-buffer option to config
      'Void': 'void'
    }

    templates = dict(
        module     = '''
          %<dependencies:lines>
          public class Program
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
                %<attrs:lines>
                %<.constructor>
                %<methods:lines>}''',

        class_definition_base = (': %<base>', ''),

        class_definiton_constructor = ('%<constructor>', ''),

        class_attr = '%<.is_public>%<@pseudo_type> %<name>;',

        class_attr_is_public = ('public ', 'private '),
        
        anonymous_function = '(%<#params>) => %<#anon_block>',

        constructor = '''
            %<this>(%<#params>)
            {
                %<block:semi>}''',

        dependency  = 'using %<name>;',


        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_double>',
        boolean     = '%<value>',
        null        = 'null',

        list        = "new %<@pseudo_type> {%<elements:join ', '>}",
        dictionary  = "new %<@pseudo_type> { %<pairs:join ', '> }",
        pair        = "{%<key>, %<value>}",
        attr        = "%<object>.%<attr>",

        assignment  = switch('first_mention',
            true       = 'var %<target> = %<value>', # in v0.3 add config/use var only for generic types
            _otherwise = '%<target> = %<value>'
        ),

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        throw_statement = 'throw %<exception>(%<value>)',

        if_statement    = '''
            if (%<test>)
            {
                %<block:semi>
            }
            %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>)
            {
                %<block:semi>
            }
            %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else 
            {
                %<block:semi>
            }''',

        while_statement = '''
            while (%<test>)
            {
                %<block:semi>
            }''',

        try_statement = '''
            try
            {
                %<block:semi>
            }
            %<handlers:lines>''',

        exception_handler = '''
            except %<exception> as %<instance>
            {
                %<block:semi>''',

        for_each_statement = '''
            for %<iterator> in %<sequence>:
                %<#block>''',
    
        for_each_with_index_statement = '''
            for %<index>, %<iterator> in %<.sequence>:
                %<#block>''',

        for_each_with_index_statement_sequence = ('%<#index_sequence>', ''),

        for_each_in_zip_statement = '''
            for %<iterators:join ', '> in zip(%<sequences:join ', '>):
                %<#block>''',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index            = '%<sequence>[%<index>]',

        index_assignment = '%<sequence>[%<index>] = %<value>',

        constant = '%<constant> = %<init>',

        regex = '@"%<value>',

        for_statement = '''
            foreach(%<iterators> in %<sequences>) {
                %<#block>}''',
        
        for_range_statement = '''
            for (int %<index> = %<.first>; %<index> != %<last>; %<index> += %<.step>)
            {
                %<block:lines>}''',

        for_range_statement_first = ('%<first>, ', ''),

        for_range_statement_step = (', %<step>', ''),

        for_iterator = 'var %<iterator>',

        for_iterator_zip = "var %<iterators:join ', '>",

        for_iterator_with_index = 'int %<index>, var %<iterator>',

        for_iterator_with_items = '%<key>, %<value>',

        custom_exception = '''
            class %<name> : Exception
        ''',

        block = '%<block:semi>'
    )
