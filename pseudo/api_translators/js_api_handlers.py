from pseudo.pseudo_tree import Node, call, method_call, local, assignment, attr, to_node

def empty(f, _):
    return Node('comparison',
        op='==',
        left=attr(f, 'length', pseudo_type='Int'),
        right=to_node(0),
        pseudo_type='Boolean')

def present(f, _):
    return Node('comparison',
        op='>',
        left=attr(f, 'length', pseudo_type='Int'),
        right=to_node(0),
        pseudo_type='Boolean')