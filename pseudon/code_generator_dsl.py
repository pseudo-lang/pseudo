import yaml
from pseudon.pseudon_tree import Node
Iterable = (list, tuple, set)

class FragmentGenerator:
    @property
    def y(self):
        result = yaml.dump(self)
        return result.replace('!python/object:pseudon.code_generator_dsl.', '')

    # we can't set __str__ and __repr__ because this makes yaml.dump insane :(
    # and i like yaml.dump, I don't want it to be insane, even if that's cute



class Placeholder(FragmentGenerator):
    def __init__(self, field):
        self.field = field

    def expand(self, generator, node, depth):
        content = getattr(node, self.field)
        if isinstance(content, Iterable):
            if not content:
                return ''
            expanded = [generator._generate_node(content[0], depth)]
            expanded += [generator.offset(depth) + generator._generate_node(node, depth) for node in content[1:]]
            return '\n'.join(expanded) + '\n'
        elif isinstance(content, Node):
            return generator._generate_node(content, depth)
        else:
            return str(content)


class PseudonType(FragmentGenerator):
    def __init__(self, type):
        self.type = type
    
    def expand(self, generator, node, depth):
        t = getattr(node, self.type)
        return self.expand_type(t, generator)

    def expand_type(self, t, generator):
        if '[' in t:
            base, _, right = t[:-1].partition('[')
            args = right.split(', ')
            return generator.types[base].format(*args)
        elif t in generator.types:
            return generator.types[t]
        else:
            return t

class Action(FragmentGenerator):
    def __init__(self, field, action, args):
        self.field = field
        self.action = action
        self.args = args

    def expand(self, generator, node, depth):
        content = getattr(node, self.field)
        if isinstance(content, Iterable):
            if content:
                expanded = [generator._generate_node(content[0], depth)]
                expanded += [generator.offset(depth) + generator._generate_node(a, depth) for a in content[1:]]
            else:
                expanded = []
        else:
            expanded = generator._generate_node(content, node)
        return getattr(generator, 'action_%s' % self.action)(expanded, *(self.args + [depth]))

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
        layout, default = generator._parsed_templates['%s_%s' % (self.a, self.field)]
        if not f:
            return generator._generate_from_template(
                default,node, depth)
        else:
            return generator._generate_from_template(
                layout,node, depth)

class Whitespace:
    def __init__(self, count=1, is_offset=True):
        self.count = count
        self.is_offset = is_offset

    def expand(self, size, single):
        return single * size

    def __repr__(self):
        if self.count == 1 and not self.is_offset:
            return 'INTERNAL_WHITESPACE'
        else:
            return 'OFFSET'

    __str__ = __repr__

    @property
    def y(self):
        return repr(self)

class Newline:
    def expand(self, depth):
        return '\n'

    def __repr__(self):
        return 'NEWLINE'

    __str__ = __repr__

    @property
    def y(self):
        return repr(self)

def internal_whitespace(count):
    return Whitespace(count, False)

Offset = Whitespace
INTERNAL_WHITESPACE = Whitespace(1, False)
NEWLINE = Newline()
