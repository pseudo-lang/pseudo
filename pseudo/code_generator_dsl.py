import yaml
from pseudo.pseudo_tree import Node
Iterable = (list, tuple, set)

class FragmentGenerator:
    @property
    def y(self):
        result = yaml.dump(self)
        return result.replace('!python/object:pseudo.code_generator_dsl.', '')

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


class PseudoType(FragmentGenerator):
    def __init__(self, placeholder):
        self.placeholder = placeholder
    
    def expand(self, generator, node, depth):
        current = node
        for t in self.placeholder:
            current = getattr(current, t)
        # print(node.type, current, self.placeholder, node.y)
        return self.expand_type(current, generator)

    def expand_type(self, t, generator):
        if isinstance(t, list):
            if t[0] == 'Tuple':
                return generator.types['Tuple']([self.expand_type(base, generator) for base in t[1:]])
            else:
                return generator.types[t[0]].format(*[self.expand_type(base, generator) for base in t[1:]])
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
        if self.action in ['join', 'join_lws', 'each_lpad', 'each_rpad'] and self.args and self.args[0] != '\n':
            depth = 0

        if isinstance(content, Iterable):
            if content:
                expanded = [generator._generate_node(content[0], depth)]
                # print(content[0].y)
                # print(self.field)
                # print(node.y)
                # input(self.action)
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
        # if not hasattr(node, self.field):
        #     print(self.field)
        f = getattr(node, self.field, None)
        layout, default = generator._parsed_templates['%s_%s' % (self.a, self.field)]
        if not f:
            # input(default)
        
            return generator._generate_from_template(
                default,node, depth)
        else:
            return generator._generate_from_template(
                layout,node, depth)

class SubElement(FragmentGenerator):
    def __init__(self, elements):
        self.elements = elements

    def expand(self, generator, node, depth):
        current = node
        for e in self.elements:
            current = getattr(current, e)
        # print(self.elements, current)
        if isinstance(current, Node):
            return generator._generate_node(current, depth)
        else:
            return current

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
