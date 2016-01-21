from pseudon.code_generator import CodeGenerator, indented


class CppGenerator(CodeGenerator):
    '''Cpp code generator'''

    def namespace(self, node, indent):
        return self.name.capitalize()

    def header(self, node, indent):
        return 'using System;\nnamespace %s;\n{\n' % self.namespace()

    templates = {
        'program': indented('''
                   %<#header>
                     %<code>
                     %<main>
                   }
                   '''),

        'main':    indented('''
                   class %<#namespace>
                   {
                     static void Main()
                     {
                       %<body>
                     }
                   }
                   '''),

        'function': indented('''
                    %<return_type> %<name>(%<args:join ','>)
                    {
                      %<body>
                    }
                    '''),

        'class': indented('''
                  class %<name> %?<:%<parent>>
                  {
                    %<methods>
                  }'''),

        'name': '%<label>',

        'int': '%<value>'
    }
