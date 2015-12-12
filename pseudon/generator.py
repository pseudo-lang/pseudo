# base generator with common functionality
class Generator:
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
        if not isinstance(node, dict):
            return node
        elif 'type' not in node:
            return node
        elif node['type'] in self.templates:
            return self._generate_from_template(self.templates[node['type']], node, depth)
        elif hasattr(self, 'generate_%s' % node['type']):
            return getattr(self, 'generate_%s' % node['type'])(node, depth)
        else:
            raise NotImplementedError("no action for %s" % node['type'])
