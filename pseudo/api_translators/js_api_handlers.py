from pseudo.pseudo_tree import Node, call, method_call, local, assignment, attr, to_node, typename

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

def object_len(l, _):
    return attr(
        method_call(
            typename('Object', 'Type'),
            'keys',
            [l],
            ['List', l.pseudo_type[1]]),
        'length',
        'Int')
