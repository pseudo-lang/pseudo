import yaml

class Node:
    '''
    A pseudo tree node

    Example: Node('local', name='l')
    '''

    def __init__(self, type, **fields):
        self.type = type
        self.__dict__.update(fields)
        if 'pseudo_type' not in fields:
            self.pseudo_type = 'Void'

    # debugging
    # and no, __dict__ is not good enough
    @property
    def y(self):
        result = yaml.dump(self)
        return result.replace('!python/object:pseudo.pseudo_tree.', '')

    def __eq__(self, a):
        return all(getattr(self, f) == getattr(a, f, None) for f in self.__dict__)

def node_representer(dumper, data):
    return dumper.represent_scalar('!%s' % type(data).__name__, )
# helpers


def method_call(receiver, message, args, pseudo_type=None):
    '''A shortcut for a method call, expands a str receiver to a identifier'''

    if not isinstance(receiver, Node):
        receiver = local(receiver)
    return Node('method_call', receiver=receiver, message=message, args=args, pseudo_type=pseudo_type)


def call(function, args, pseudo_type=None):
    '''A shortcut for a call with an identifier callee'''

    if not isinstance(function, Node):
        function = local(function)
    return Node('call', function=function, args=args, pseudo_type=pseudo_type)

def local(name, pseudo_type=None):
    return Node('local', name=name, pseudo_type=pseudo_type)

def typename(name, pseudo_type=None):
    return Node('typename', name=name, pseudo_type=pseudo_type)

def if_statement(test, block, otherwise):
    return Node('if', test=test, block=block, otherwise=otherwise, pseudo_type='Void')

def index_assignment(sequence, index, value):
    return Node('index_assignment', sequence=sequence, index=index, value=value, pseudo_type='Void')

def for_each_with_index_statement(iterators, sequence, block):
    return Node('for_each_with_index', iterators=iterators, sequence=sequence, block=block)

def assignment(target, value, first_mention=None):
    ass = Node('assignment', target=target, value=value, pseudo_type='Void')
    if first_mention is not None:
        ass.first_mention = first_mention
    return ass

def attr(value, attr, pseudo_type=None):
    return Node('attr', object=value, attr=attr, pseudo_type=pseudo_type)

def for_each(iterator, sequence, block):
    return Node('for_statement', iterators=Node('for_iterator', iterator=iterator), 
                sequences=Node('for_sequence', sequence=sequence), 
                block=block, pseudo_type='Void')

def to_node(value):
    '''Expand to a literal node if a basic type otherwise just returns the node'''

    if isinstance(value, Node):
        return value
    elif isinstance(value, str):
        return Node('string', value=value, pseudo_type='String')
    elif isinstance(value, int):
        return Node('int', value=value, pseudo_type='Int')
    elif isinstance(value, bool):
        return Node('boolean', value=str(value).lower(), pseudo_type='Boolean')
    elif isinstance(value, float):
        return Node('float', value=value, pseudo_type='Float')
    elif value is None:
        return Node('null', pseudo_type='Void')
    else:
        1/0

