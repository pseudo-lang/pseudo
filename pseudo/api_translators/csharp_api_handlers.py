from pseudo.pseudo_tree import Node, call, method_call, local, assignment, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

def expand_slice(receiver, from_, to, pseudo_type=None):
    return method_call(method_call(receiver, 'Take', [to], pseudo_type), 'Drop', [from_], pseudo_type)
