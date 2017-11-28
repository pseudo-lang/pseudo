from pseudo.code_generator import CodeGenerator, switch
from pseudo.middlewares import GoConstructorMiddleware, TupleMiddleware, DeclarationMiddleware, NameMiddleware, StandardMiddleware # GoErrorHandlingMiddleware
from pseudo.code_generator_dsl import PseudoType
from pseudo.pseudo_tree import Node, local
from pseudo.helpers import general_type, safe_serialize_type

OPS = {'not': '!', 'or': '||', 'and': '&&'}

class GolangGenerator(CodeGenerator):
    '''Go generator'''

    indent = 1
    use_spaces = False

    middlewares = [TupleMiddleware(True), 
        GoConstructorMiddleware,
        DeclarationMiddleware, 
        NameMiddleware(
            normal_name='camel_case',
            method_name='pascal_case',
            function_name='pascal_case',
            attr_name='pascal_case'),
        StandardMiddleware] # GoErrorHandlingMiddleware
    
    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': '[]{0}',
      'Dictionary': 'map[{0}]{1}',
      'Set': 'map[{0}]struct{}',
      'Tuple': lambda x: safe_serialize_type(['Tuple'] + x),
      # uh yea, in next version we'll add some kind of smart-name / config option
      'Array': '[{1}]{0}', 
      'Void': 'void',
      'Regexp': '*regexp.Regexp',
      'RegexpMatch': '[][][]byte'
    }

    templates = dict(
        module     = '''
          package main

          %<#dependencies>
          %<constants:lines>
          %<custom_exceptions:lines>
          %<definitions:lines>
          %<tuple_definitions:line_join>
          func main() {
              %<main:line_join>
          }''',

        function_definition   = '''
            func %<name>(%<#params>) %<#return_type> {
                %<block:line_join>
            }''',

        method_definition =     '''
            func (this *%<this>) %<name>(%<#params>) %<#return_type> {
                %<block:line_join>
            }''',

        class_definition = '''
            type %<name> struct {
               %<.base>
               %<attrs:line_join>
            }

            %<.constructor>
            %<methods:line_join>''',

        class_definition_base = ('extend %<base>', ''),

        class_definition_constructor = ('%<constructor>', ''),

        class_attr = switch('is_public',
            true         = "%<name> %<@pseudo_type>",
            _otherwise   = "%<name> %<@pseudo_type>"),

        immutable_class_attr = "%<name:camel_case 'title'> %<@pseudo_type>",

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

        _go_bytes = '[]byte(%<value>)',

        _go_make_slice = 'make(%<@slice_type>, %<#initial>, %<length>)',

        _go_simple_initializer = "%<name>{%<args:join ', '>}",

        _go_declaration = 'var %<decl> %<@decl_type>',

        dependency  = '"%<name>"',

        break_      = 'break',

        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_double>',
        boolean     = '%<value>',
        null        = 'nil',

        list        = switch(lambda l: len(l.elements) > 0,
                        true        = "%<@pseudo_type> {%<elements:join ', '>}",
                        _otherwise  = "[]int {}"
                    ),
        dictionary  = switch(lambda l: len(l.pairs) > 0,
                        true        = "%<@pseudo_type> { %<pairs:join ', '> }",
                        _otherwise  = "map[int]int {}"
                    ),
        pair        = "%<key>: %<value>",
        attr        = "%<object>.%<attr>",
        array       = "[...]%<#element_type>{%<elements:join ', '>}",

        _go_slice      = '%<sequence>[%<from_>:%<to>]',
        _go_slice_from = '%<sequence>[%<from_>:]',
        _go_slice_to   = '%<sequence>[:%<to>]',

        assignment  = switch('first_mention',
            true       = '%<target> := %<value>',
            _otherwise = '%<target> = %<value>'
        ),

        _go_multi_assignment = switch('first_mention',
            true       = "%<targets:join ', '> := %<values:join ', '>",
            _otherwise = "%<targets:join ', '> = %<values:join ', '>"
        ),

        _go_ref     = '&%<value>',

        binary_op   = '%<#binary_left> %<#op> %<#binary_right>',
        unary_op    = '%<#op>%<value>',
        comparison  = '%<#binary_left> %<op> %<#binary_right>',

        set         = switch(lambda l: len(l.elements) > 0,
                        true        = "%<@pseudo_type> { #set_pairs }",
                        _otherwise  = "map[int]struct{} {}"
                    ),
        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",
        this_method_call = "this.%<message>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this.%<name>',

        not_null_check = 'false', #'%<value> != nil',

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
            for %<index> := %<.first>; %<index> != %<end>; %<index> += %<.step> {
                %<block:line_join>
            }''',

        for_range_statement_first = ('%<start>', '0'),

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

        aug_assignment =  '%<target> %<op>= %<value>',

        index            = switch(lambda i: i.index.type != 'int' or i.index.value >= 0,
                                true        = '%<sequence>[%<index>]',
                                _otherwise  = '%<sequence>[len(%<sequence>) - %<#index>]'),

        interpolation =     "fmt.Sprintf(\"%<args:join ''>\", %<#placeholderz>)",

        interpolation_literal = '%<value>',
        
        interpolation_placeholder = switch(lambda i: i.pseudo_type == 'Int',
            true        = '%d',
            _otherwise  = '%s'),

        index_assignment = '%<sequence>[%<index>] = %<value>',

        constant = '%<constant> = %<init>',


        custom_exception = '''
            class %<name> : Exception
        ''',

        simple_initializer = "%<name>{%<args:join ', '>}",

        standard_iterable_call = '''
            var _results %<@pseudo_type>
            for %<iterators> := range %<sequences> {
                if %<test:first> {
                    _results = append(_results, %<block:first>)
                }
            }
            _results''',

        standard_iterable_call_return = '''
            var _results %<@pseudo_type>
            for %<iterators> := range %<sequences> {
                if %<test:first> {
                    _results = append(_results, %<block:first>)
                }
            }
            return _results''',

        block = '%<block:line_join>',

        regex = '"%<value>"',
    )
    
    def params(self, node, depth):
        return ', '.join(
            '%s %s' % (
              self._generate_node(k),
              self.render_type(node.pseudo_type[j + 1]))
              for j, k in enumerate(node.params))

    def dependencies(self, node, depth):
        if len(node.dependencies) == 1:
            return 'import "%s"' % node.dependencies[0].name
        elif len(node.dependencies) > 1:
            return 'import (\n\t%s\n)\n' % '\n\t'.join('"%s"' % q.name for q in node.dependencies)
        else:
            return ''

    def element_type(self, node, _):
        return PseudoType('').expand_type(node.pseudo_type[1], self)

    def op(self, node, depth):
        return OPS.get(node.op, node.op)

    # keys in pseudo can be only string or int float bool
    def initial(self, node, _):
        '''initial value for make'''
        return {'Int': '0', 'Float': '0.0', 'String': '""', 'Bool': 'true'}.get(node.slice_type[1], 'nil')

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

    def placeholderz(self, node, _):
        return ', '.join(self._generate_node(placeholder.value) for placeholder in node.args[1::2])

    def index(self, node, depth):
        return str(-node.index.value)

    def return_type(self, node, depth):
        format = self.render_type(node.return_type)
        if isinstance(node.return_type, list) or node.return_type in self.types:
            return format
        else:
            return '*%s' % format
