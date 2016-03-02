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

    templates = dict(
        module         = '%<dependencies:lines>%<definitions:lines>%<main:lines>',

        function_definition = '''
            def %<name>%<.args>
              %<body:lines>
            end
            ''',

        function_definition_args = ("(%<args:join ', '>)", ''),

        class_definition     = '''
            class %<name>%<.parent>
              %<methods:lines>
            end
            ''',

        class_definition_parent = ('< %<parent>', ''),

        local           = '%<name>',
        int             = '%<value>',
        float           = '%<value>',
        string          = '%<#safe_single>',
        boolean         = '%<value>',
        null            = 'nil',

        list            = "[%<elements:join ', '>]",
        dict            = '{%<#ruby_dict>}'
    )
