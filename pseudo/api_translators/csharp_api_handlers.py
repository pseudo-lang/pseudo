from pseudo.pseudo_tree import Node, call, method_call, typename, to_node, attr
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

def normalize(f, from_, to):
    if to.type == 'int':
        if to.value < 0:
            if from_.type != 'int':
                return Node('binary_op',
                    op='-', 
                    left=Node('binary_op',
                        op='-',
                        left=attr(f, 'Length', 'Int'),
                        right=to,
                        pseudo_type='Int'),
                    right=from_,
                    pseudo_type='Int')
            else:
                return Node('binary_op',
                    op='-', 
                    left=attr(f, 'Length', 'Int'),
                    right=to_node(-to.value + from_.value),
                    pseudo_type='Int')
        else:
            if from_.type != 'int':
                return Node('binary_op',
                    op='-', 
                    left=to,
                    right=from_,
                    pseudo_type='Int')
            else:
                return to_node(to.value - from_.value)

def pad(f, count, fill, _):
    return method_call(
        method_call(
            f,
            'PadLeft',
            [Node('binary_op',
                op='+',
                left=Node('binary_op',
                    op='/',
                    left=Node('binary_op',
                        op='-',
                        left=count,
                        right=attr(f, 'Length', 'Int'),
                        pseudo_type='Int'),
                    right=to_node(2),
                    pseudo_type='Int'),
                right=attr(f, 'Length', 'Int'),
                pseudo_type='Int'),
            fill],
            pseudo_type='String'),
        'PadRight',
        [count, fill],
        'String')

def expand_slice(receiver, from_, to, pseudo_type=None):
    return method_call(method_call(receiver, 'Take', [to], pseudo_type), 'Drop', [from_], pseudo_type)

class Display(NormalLeakingNode):
    def as_expression(self):
        return [Node('static_call',
                    receiver=typename('Console', 'Library'),
                    message='WriteLine',
                    args=[arg],
                    pseudo_type='Void')
                for arg
                in self.args], None

