from pseudon.code_generator import CodeGenerator, join, indent, eventually


class CSharpGenerator(CodeGenerator):

	def namespace(self):
		return self.name.capitalize()

	def header(self):
		return 'using System;\n' +\
			   'namespace %s;\n{\n' % self.namespace() +\

    templates = {
        'program': [self.header, indent('code', 1), indent('main', 1), '}\n'],
        'main': [lambda self: 'class %s\n{\n' % self.namespace(), 
                 '%{offset1}static void Main()\n%{offset1}{\n', 
                 indent('body', 1), '\n%{offset1}}\n%{offset}}\n'],
        'function': ['%{return_type} %{name}(', join('args', ','), '){\n',
                     indent('body', 1), '\n}\n'],
        'class': ['class %{name}', eventually('parent', ' :%{parent}'), '{\n',
                  indent('methods', 1), '\n}\n'],
        'name': '%{label}',
        'int': '%{value}'
    }
