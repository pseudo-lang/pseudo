from pseudo.code_generator import CodeGenerator, switch
from pseudo.middlewares import DeclarationMiddleware, CppPointerMiddleware, CppDisplayExceptionMiddleware
from pseudo.pseudo_tree import Node, local
from pseudo.code_generator_dsl import PseudoType

class CppGenerator(CodeGenerator):
    '''Cpp code generator'''

    indent = 4
    use_spaces = True

    middlewares = [DeclarationMiddleware, CppPointerMiddleware, CppDisplayExceptionMiddleware]

    types = {
      'Int': 'int',
      'Float': 'float',
      'Boolean': 'bool',
      'String': 'string',
      'List': 'vector<{0}>',
      'Dictionary': 'unordered_map<{0}, {1}>',
      'Tuple': lambda t: 'pair<{0}{1}>'.format(*t) if len(t) == 2 else 'tuple<{0}>'.format(', '.join(t)),
      'Array': '{0}*',
      'Set': 'set<{0}>',
      'Void': 'void',
      'Pointer': 'smart_ptr<{0}>'
    }

    templates = dict(
        module     = '''
          %<dependencies:lines>
          %<#exception_dependencies>
          %<constants:lines>
          %<custom_exceptions:lines>
          %<definitions:lines>
          int main() {
              %<main:semi>
          }
          ''',

        function_definition   = '''
            %<@return_type> %<name>(%<#params>) {
                %<block:semi>
            }''',

        method_definition =     '''
            %<@return_type> %<name>(%<#params>) {
                %<block:semi>
            }''',

        class_definition = '''
              class %<name>%<.base> {
                  %<attrs:lines>
                  %<.constructor>
                  %<methods:lines>
              }''',

        class_definition_base = (': %<base>', ''),

        class_definition_constructor = ('%<constructor>', ''),

        class_attr = '%<.is_public> %<@pseudo_type> %<name>;',

        class_attr_is_public = ('public', 'private'),

        anonymous_function = '[](%<#params>) %<#anon_block>',

        constructor = '''
            %<this>(%<#params>) {
                %<block:semi>
            }''',

        dependency  = '#include<%<name>>',


        local       = '%<name>',
        typename    = '%<name>',
        int         = '%<value>',
        float       = '%<value>',
        string      = '%<#safe_double>',
        boolean     = '%<value>',
        null        = 'NULL',

        list        = "{%<elements:join ', '>}",
        dictionary  = "%<@pseudo_type>{{%<pairs:join ', '>}}",
        set         = "%<@pseudo_type>({%<elements:join ', '>})",
        regex       = 'regex("%<value>")',
        pair        = "%<key>: %<value>",
        attr        = "%<object>.%<attr>",

        assignment    = switch('first_mention',
          true = '%<@value.pseudo_type> %<target> = %<value>',
          _otherwise = '%<target> = %<value>'
        ),

        binary_op   = '%<left> %<op> %<right>',
        unary_op    = '%<op>%<value>',
        comparison  = '%<left> %<op> %<right>',

        static_call = "%<receiver>.%<message>(%<args:join ', '>)",
        call        = "%<function>(%<args:join ', '>)",
        method_call = "%<receiver>.%<message>(%<args:join ', '>)",  
        pointer_method_call = "%<receiver>->%<message>(%<args:join ', '>)",

        this        = 'this',

        instance_variable = 'this->%<name>',

        new_instance    = "new %<class_name>(%<args:join ', '>)",

        throw_statement = 'throw %<exception>(%<value>)',

        if_statement    = '''
            if (%<test>) {
                %<block:semi>
            } %<.otherwise>''',

        if_statement_otherwise = ('%<otherwise>', ''),

        elseif_statement = '''
            else if (%<test>) {
                %<block:semi>
            } %<.otherwise>''',

        elseif_statement_otherwise = ('%<otherwise>', ''),

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
            }
            %<handlers:lines>''',

        exception_handler = '''
            catch (%<.exception>& %<instance>) {
                %<block:semi>
            }''',

        exception_handler_exception = ('%<exception>', 'exception'),

        for_statement = switch(lambda f: f.iterators.type,
            for_iterator_with_index = '''
                for(int %<iterators.index> = 0; %<iterators.index> < %<sequences.sequence>.size(); %<iterators.index> ++) {
                    auto %<iterators.iterator> = %<sequences.sequence>[%<iterators.index>];
                    %<block:semi>
                }''',

            for_iterator_zip = '''
                for(int _index = 0; _index < %<#first_sequence>.size(); _index ++) {
                    %<#zip_iterators>
                    %<block:semi>
                }''',

            for_iterator_with_items = '''
                for(auto& _item : %<sequences.sequence>) {
                    auto %<iterators.key> = _item.first;
                    auto %<iterators.value> = _item.second;
                    %<block:semi>
                }''',
            _otherwise = '''
                for(%<iterators>: %<sequences>) {
                    %<block:semi>
                }'''
        
        ),
        
        for_range_statement = '''
            for(int %<index> = %<.first>; %<index> != %<end>; %<index> += %<.step>) {
                %<block:semi>
            }''',

        for_range_statement_first = ('%<start>', '0'),

        for_range_statement_step = ('%<step>', '1'),

        for_iterator = 'auto %<iterator>',

        for_iterator_zip = "var %<iterators:join ', '>",

        for_iterator_with_index = 'int %<index>, var %<iterator>',

        for_iterator_with_items = '%<key>, %<value>',

        for_sequence = '%<sequence>',

        implicit_return = 'return %<value>',
        explicit_return = 'return %<value>',

        _with = '''
            with %<call> as %<context>:
                %<block:semi>''',

        index = '%<sequence>[%<index>]',

        block = '%<block:semi>',

        custom_exception = '''
            class %<name> : runtime_error {
            }''',

        _cpp_declaration = '%<@decl_type> %<name>%<.args>',

        _cpp_declaration_args = ("(%<args:join ', '>)", ''),

        _cpp_anon_declaration = "%<@decl_type>(%<args:join ', '>)",

        _cpp_group = '(%<value>)',

        _cpp_cin = 'cin >> %<args:first>', # support only one for now

        _cpp_cout = "cout << %<args:join ' << '> << endl"
    )
  
    def namespace(self, node, indent):
        return self.name.capitalize()

    def header(self, node, indent):
        return 'using System;\nnamespace %s;\n{\n' % self.namespace()

    def params(self, node, indent):
        return ', '.join(
            '%s %s' % (
              PseudoType('').expand_type(k.pseudo_type, self),
              k.name) for j, k in enumerate(node.params) )

    def anon_block(self, node, indent):
        if len(node.block) == 1:
            b = self._generate_node(node.block[0])
            return '{ %s; }' % b
        else:
            b = ';\n'.join(self.offset(indent + 1) + self._generate_node(e, indent + 1) for e in node.block) + ';'
            return '{\n%s\n%s}' % (b, self.offset(indent))

  
    def exception_dependencies(self, node, indent):
        if node.custom_exceptions:
            iostream = ''
            for d in node.dependencies:
                if d.name == 'iostream':
                    break
            else:
                iostream = '#include<iostream>\n'
            return '%s#include<stdexcept>\n#include<exception>\n' % iostream
        else:
          return ''

    def zip_iterators(self, node, depth):
        return '\n'.join(
            '%sauto %s = %s;' % (
                self.offset(depth) if j else '',
                q.name,
                self._generate_node(
                    Node('index',
                        sequence=node.sequences.sequences[j],
                        index=local('_index', 'Int'),
                        pseudo_type=node.sequences.sequences[j].pseudo_type[1])))
            for j, q 
            in enumerate(node.iterators.iterators))

    def first_sequence(self, node, depth):
        return self._generate_node(node.sequences.sequences[0])
