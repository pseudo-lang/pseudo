# base generator with common functionality
import re
from pseudon.pseudon_tree import Node


class CodeGenerator:
    '''
    options:
      indent: the size of indent, example: python - 4, ruby - 2
      spaces: use spaces if true, tabs if false
    '''

    def __init__(self, indent=4, spaces=True):
        self.indent = indent
        self.spaces = spaces

    def generate(self, tree):
        '''
        generates code based on templates and gen functions
        defined in the <x> lang generator
        '''
        return self._generate_node(tree, 0)

    def _generate_node(self, node, depth=0):
        if not isinstance(node, Node):
            return node
        elif node.type in self.templates:
            return self._generate_from_template(self.templates[node.type], node, depth)
        elif hasattr(self, 'generate_%s' % node['type']):
            return getattr(self, 'generate_%s' % node['type'])(node, depth)
        else:
            raise NotImplementedError("no action for %s" % node['type'])

    def _generate_from_template(self, template, node, depth):
        if not isinstance(template, list):
            template = [template]  # cleaner dsl

        expanded = []
        expanded.append(self._offset(depth))
        for i, element in enumerate(template):
            if i > 0:
                depth = 0
            if isinstance(element, str):
                expanded.append(self._expand_string(element, node, depth))
            elif callable(element):
                expanded.append(element(node, depth))
            elif isinstance(element, TemplateEventually):
                expanded.append(element.expand(
                    node, depth, self._expand_string, self._generate_node))
            elif isinstance(element, TemplateFunction):
                expanded.append(element.expand(
                    node, depth, self._offset, self._generate_node))

        return ''.join(expanded)

    def _offset(self, depth):
        return (' ' if self.spaces else '\t') * (self.indent * depth)

    def _expand_string(self, template, node, depth):
        return re.sub(r'%\{(\w+)\}',
                      lambda match: self._generate_node(gettatr(node, match.group(
                          1)), 0) if match.group(1) != 'indent' else self._offset(depth),
                      template)


class TemplateFunction:

    def expand(node, depth, offset_function, generate):
        pass


class TemplateJoin(TemplateFunction):

    def __init__(self, field, delimiter):
        self.field = field
        self.delimiter = delimiter

    def expand(self, node, depth, offset_function, generate):
        f = generate(getattr(node, self.field), depth)
        print(f)
        return self.delimiter.join(generate(getattr(node, self.field), depth))


class TemplateIndent(TemplateFunction):

    def __init__(self, field, depth, end_symbol):
        self.field = field
        self.depth = depth
        self.end_symbol = end_symbol

    def expand(self, node, depth, offset_function, generate):
        q = generate(getattr(node, self.field))
        return '\n'.join('%s%s' % (offset_function(depth + self.depth), a) for a in q) + '\n'


class TemplateEventually(TemplateFunction):

    def __init__(self, field, template):
        self.field = field
        self.template = template

    def expand(self, node, depth, expand_to_string_function, generate):
        if getattr(node, self.field):
            return expand_to_string_function(self.template, node, depth)
        else:
            return ''


def join(field, delimiter):
    return TemplateJoin(field, delimiter)


def indent(field, depth, end_symbol=''):
    return TemplateIndent(field, depth, end_symbol)


def eventually(field, template):
    return TemplateEventually(field, template)
