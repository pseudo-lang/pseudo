from pseudon.pseudon_tree import Node, call, method_call, local, assignment, to_node

def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if to:
            return Node('_rb_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            return Node('_rb_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_rb_slice', sequence=receiver, from_=to_node(0), to=to, pseudo_type=pseudo_type)
    else:
        return None

