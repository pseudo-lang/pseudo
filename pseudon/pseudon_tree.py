class Node:
    '''
    A pseudon tree node

    Example: Node('local', name='l')
    '''

    def __init__(self, type, fields):
        self.type = type
        self.__dict__.update(fields)


# helpers


def method_call(receiver, message, args):
    '''A shortcut for a method call, expands a str receiver to a identifier'''

    return Node('method_call', receiver=to_node(receiver), message=message, args=args)


def call(callee, args):
    '''A shortcut for a call with an identifier callee'''

    return Node('call', callee=to_node(callee), args=args)


def to_node(name):
    '''Expand to a literal node if a basic type otherwise just returns the node'''

    if isinstance(name, Node):
        return name
    elif isinstance(name, str):
        return Node('local', name) if name[0].islower() else Node('typename', name)
    elif isinstance(name, int):
        return Node('int', name)
