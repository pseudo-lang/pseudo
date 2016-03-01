from pseudon.code_generator import CodeGenerator


class CSharpGenerator(CodeGenerator):
    '''CSharp code generator'''

    indent = 4
    use_spaces = True

    def namespace(self, node, indent):
        return self.name.capitalize()

    def header(self, node, indent):
        return 'using System;\nnamespace %s;\n{\n' % self.namespace(node, indent)

    templates = {
        'program': '''
                   %<#header>
                     %<code>
                     %<main>
                   }
                   ''',

        'main':    '''
                   class %<#namespace>
                   {
                     static void Main()
                     {
                       %<body>
                     }
                   }
                   ''',

        'function': '''
                    %<return_type> %<name>(%<args:join ','>)
                    {
                      %<body>
                    }
                    ''',

        'class': '''
                  class %<name>%<.parent>
                  {
                    %<methods>
                  }''',

        'class.parent': ' :%<parent>',

        'name': '%<label>',

        'int': '%<value>'
    }
