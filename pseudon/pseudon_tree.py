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


def method_call(receiver, message, args, pseudo_type=None):
    '''A shortcut for a method call, expands a str receiver to a identifier'''

    return Node('method_call', receiver=to_node(receiver), message=message, args=args, pseudo_type=pseudo_type)


def call(function, args, pseudo_type=None):
    '''A shortcut for a call with an identifier callee'''

    return Node('call', function=to_node(function), args=args, pseudo_type=pseudo_type)

def local(name, pseudo_type=None):
    return Node('local', name=name, pseudo_type=pseudo_type)

def if_statement(test, block, otherwise):
    return Node('if', test=test, block=block, otherwise=otherwise, pseudo_type='Void')

def index_assignment(sequence, index, value):
    return Node('index_assignment', sequence=sequence, index=index, value=value, pseudo_type='Void')

def for_each_with_index_statement(iterators, sequence, block):
    return Node('for_each_with_index', iterators=iterators, sequence=sequence, block=block)

def local_assignment(local, value, value_type=None):
    return Node('local_assignment', local=local, value=value, pseudo_type='Void', value_type=value_type)

def attr(value, attr, pseudo_type=None):
    return Node('attr', value=value, attr=attr, pseudo_type=pseudo_type)

def for_each(iterator, sequence, block):
    return Node('for_statement', iterators=Node('for_iterator', iterator=iterator), 
                sequences=Node('for_sequence', sequence=sequence), 
                block=block, pseudo_type='Void')

def to_node(name):
    '''Expand to a literal node if a basic type otherwise just returns the node'''

    if isinstance(name, Node):
        return name
    elif isinstance(name, str):
        if name[0] == '"':
            return Node('string', value=name[1:-1], pseudo_type='String')
        elif name[0].islower():
            return Node('local', name=name)
        else:
            return Node('typename', name=name)

    elif isinstance(name, int):
        return Node('int', value=name, pseudo_type='Int')
    elif isinstance(name, bool):
        return Node('boolean', value=str(name).lower(), pseudo_type='Boolean')
    elif isinstance(name, float):
        return Node('float', value=name, pseudo_type='Float')
    else:
        1/0

def assignment_updated(assignment, **kwargs):
    ass = Node(assignment.type)
    ass.__dict__.update(assignment.__dict__)
    ass.__dict__.update(kwargs)
    return ass
