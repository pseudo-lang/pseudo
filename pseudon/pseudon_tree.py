import yaml

class Node:
    '''
    A pseudon tree node

    Example: Node('local', name='l')
    '''

    def __init__(self, type, **fields):
        self.type = type
        self.__dict__.update(fields)

    # and no, __dict__ is not good enough
    @property
    def y(self):
        result = yaml.dump(self)
        return result.replace('!python/object:pseudon.pseudon_tree.', '')

def node_representer(dumper, data):
    return dumper.represent_scalar('!%s' % type(data).__name__, )
# helpers


def method_call(receiver, message, args):
    '''A shortcut for a method call, expands a str receiver to a identifier'''

    return Node('method_call', receiver=to_node(receiver), message=message, args=args)


def call(function, args):
    '''A shortcut for a call with an identifier callee'''

    return Node('call', function=to_node(function), args=args)

def local(name):
    return Node('local', name=name)

def if_statement(test, block, otherwise):
    return Node('if', test=test, block=block, otherwise=otherwise)

def item_assignment(sequence, index, value):
    return Node('_item_assignment', sequence=sequence, index=index, value=value)

def for_each_with_index_statement(iterators, sequence, block):
    return Node('for_each_with_index', iterators=iterators, sequence=sequence, block=block)

def to_node(name):
    '''Expand to a literal node if a basic type otherwise just returns the node'''

    if isinstance(name, Node):
        return name
    elif isinstance(name, str):
        if name[0] == '"':
            return Node('string', value=name[1:-1])
        elif name[0].islower():
            return Node('local', name=name)
        else:
            return Node('typename', name=name)

    elif isinstance(name, int):
        return Node('int', value=name)
    elif isinstance(name, bool):
        return Node('boolean', value=name)
    elif isinstance(name, float):
        return Node('float', value=name)
    else:
        1/0