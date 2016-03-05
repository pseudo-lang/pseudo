from pseudon.code_generator import CodeGenerator, switch
from pseudon.middlewares import GoConstructorMiddleware, TupleMiddleware, DeclarationMiddleware # GoErrorHandlingMiddleware #, GoTupleMiddleware
from pseudon.code_generator_dsl import PseudonType
from pseudon.pseudon_tree import Node, local

class GolangGenerator(CodeGenerator):
    '''Go generator'''

    indent = 1
    use_spaces = False

    middlewares = [TupleMiddleware, GoConstructorMiddleware, DeclarationMiddleware] # GoErrorHandlingMiddleware
    
    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': '[]{0}',
      'Dictionary': 'map[{0}]{1}',
      'Set': 'map[{0}]struct{}',
      'Tuple': lambda x: 'Tuple{0}'.format(', '.join(x).replace('[]', 'List').replace('[', '').replace(']', '')),
      # uh yea, in next version we'll add some kind of smart-name / config option
      'Array': '[{1}]{0}', 
      'Void': 'void'
    }

    templates = dict(
        module     = '''
          %<#dependencies>
          %<constants:lines>
          %<custom_exceptions:lines>
          %<definitions:lines>
          %<tuple_definitions:line_join>
          func main() {
              %<main:line_join>
          }''',

        function_definition   = '''
            func %<name>(%<#params>) %<@return_type> {
                %<block:line_join>
            }''',

        method_definition =     '''
            func %<name>(this *%<this>, %<#params>) %<@return_type> {
                %<block:line_join>
            }''',

        class_definition = '''
            struct %<name> {
               %<.base>
               %<attrs:lines>
            }

            %<.constructor>
            %<methods:lines>''',

        class_definition_base = ('extend %<base>', ''),

        class_definition_constructor = ('%<constructor>', ''),

        class_attr = '%<name> %<@pseudo_type>',

        anonymous_function = switch(lambda a: len(a.block) == 1,
            true        = 'func (%<#params>) { %<block:first> }',
            _otherwise  = '''
                func (%<#params>) {
                    %<block:line_join>
                }'''),


        constructor = '''
            func new%<this>(%<#params>) *%<this> {
                %<block:line_join>
            }''',

        new_instance = "new%<class_name>(%<args:join ', '>)",

        _go_simple_initializer = "%<name>{%<args:join ', '>}",

        dependency  = '"%<name>"',

        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_double>',
        boolean     = '%<value>',
        null        = 'nil',

        list        = "%<@pseudo_type> {%<elements:join ', '>}",
        dictionary  = "%<@pseudo_type> { %<pairs:join ', '> }",
        pair        = "%<key>: %<value>",
        attr        = "%<object>.%<attr>",
        array       = "{%<elements:join ', '>}",

        _go_slice      = '%<sequence>[%<from_>:%<to>]',
        _go_slice_from = '%<sequence>[%<from_>:len(%<sequence>)]',
        _go_slice_to   = '%<sequence>[0:%<to>]',
        _go_slice_     = '%<sequence>[:]',

        assignment  = switch('first_mention',
            true       = '%<target> := %<value>',
            _otherwise = '%<target> = %<value>'
        ),

        _go_multi_assignment = switch('first_mention',
            true       = "%<targets:join ', '> := %<values:join ', '>",
            _otherwise = "%<targets:join ', '> = %<values:join ', '>"
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
            if %<test> {
                %<block:line_join>
            } %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            else if %<test> {
                %<block:line_join>
            } %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

        else_statement = '''
            else {
                %<block:line_join>
            }''',

        while_statement = '''
            for %<test> {
                %<block:line_join>
            }''',

        # try_statement = '''
        #     try
        #     {
        #         %<block:semi>
        #     }
        #     %<handlers:lines>''',

        # exception_handler = '''
        #     except %<exception> as %<instance>
        #     {
        #         %<block:semi>''',

        for_statement = switch(lambda f: f.iterators.type,
            for_iterator_zip = '''
                for _index, _ := range %<sequences> {
                    %<#zip_iterators>
                    %<block:line_join>
                }
            ''',
            _otherwise = '''
                for %<iterators> := range %<sequences> {
                    %<block:line_join>
                }'''
        ),
        
        for_range_statement = '''
            for %<index> := %<.first>; %<index> != %<last>; %<index> += %<.step> {
                %<block:line_join>
            }''',

        for_range_statement_first = ('%<first>', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_iterator = '_, %<iterator>',

        for_iterator_zip = '%<#zip_iterators>',

        for_iterator_with_index = '%<index>, %<iterator>',

        for_iterator_with_items = '%<key>, %<value>',

        for_sequence = '%<sequence>',

        for_sequence_zip = 'len(%<sequences:first>)',

        for_sequence_with_index = '%<sequence>',

        for_sequence_with_items = '%<sequence>',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        index            = '%<sequence>[%<index>]',

        index_assignment = '%<sequence>[%<index>] = %<value>',

        constant = '%<constant> = %<init>',

        regex = '@"%<value>',

        custom_exception = '''
            class %<name> : Exception
        ''',

        block = '%<block:line_join>'
    )
    
    def params(self, node, depth):
        return ', '.join('%s %s' % (q.name, PseudonType('').expand_type(q.pseudo_type, self)) for q in node.params)

    def dependencies(self, node, depth):
        if len(node.dependencies) == 1:
            return 'import "%s"' % node.dependencies[0].name
        elif len(node.dependencies) > 1:
            return 'import (\n\t%s\n)\n' % '\n\t'.join('"%s"' % q.name for q in node.dependencies)
        else:
            return ''

    def zip_iterators(self, node, depth):
        return '\n'.join(
            '%s%s := %s' % (
                self.offset(depth) if j else '',
                q.name,
                self._generate_node(
                    Node('index',
                        sequence=node.sequences.sequences[j],
                        index=local('_index', 'Int'),
                        pseudo_type=node.sequences.sequences[j].pseudo_type[1])))
            for j, q 
            in enumerate(node.iterators.iterators))
