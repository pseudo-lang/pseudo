class FragmentGenerator:
    pass

class Placeholder(FragmentGenerator):
    def __init__(self, field):
        self.field = field

    def expand(self, generator, node, depth):
        content = getattr(node, self.field)
        if isinstance(content, list):
            expanded = [generator._generate_node(content[0], depth)]
            expanded += [generator._single_indent * depth + generator._generate_node(node, depth) for node in content[1:]]
            return '\n'.join(expanded) + '\n'
        else:
            return generator._generate_node(content, node)

class Action(FragmentGenerator):
    def __init__(self, field, action, args):
        self.field = field
        self.action = action
        self.args = args

    def expand(self, generator, node, depth):
        content = getattr(node, self.field)
        if isinstance(content, list):
            expanded = [generator._single_indent * depth + generator._generate_node(node, depth) for node in content]
        else:
            expanded = generator._generate_node(content, node)
        return getattr(generator, 'action_%s' % self.action)(node, *args, depth)

class Function(FragmentGenerator):
    def __init__(self, name):
        self.name = name

    def expand(self, generator, node, depth):
        return getattr(generator, self.name)(node, depth)

class SubTemplate(FragmentGenerator):
    def __init__(self, a, field):
        self.a = a
        self.field = field

    def expand(self, generator, node, depth):
        f = getattr(node, self.field)
        if f is None:
            return ''
        else:
            return generator._generate_from_template(
                generator._parsed_templates['%s.%s' % (self.a, self.field)],
                f,
                depth)

class Whitespace:
    def __init__(self, count=1, is_offset=True):
        self.count = count
        self.is_offset = is_offset

    def expand(self, size, single):
        return single * size

class Newline:
    def expand(self, depth):
        return '\n' * repeat

def internal_whitespace(count):
    return Whitespace(count, False)

Offset = Whitespace
INTERNAL_WHITESPACE = Whitespace(1, False)
NEWLINE = Newline()
