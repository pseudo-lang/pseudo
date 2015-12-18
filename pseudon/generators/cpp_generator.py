from pseudon.code_generator import CodeGenerator, indented


class CppGenerator(CodeGenerator):
    '''Cpp code generator'''

    def namespace(self, node, indent):
        return self.name.capitalize()

    def header(self, node, indent):
        return 'using System;\nnamespace %s;\n{\n' % self.namespace()

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
                  class %<name> %?<:%<parent>>
                  {
                    %<methods>
                  }''',

        'name': '%<label>',

        'int': '%<value>'
    }
