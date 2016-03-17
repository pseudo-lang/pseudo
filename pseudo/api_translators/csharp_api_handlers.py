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
    else:
        if from_.type == 'int' and from_.value == 0:
            return to
        else:
            return Node('binary_op', op='-', left=to, right=from_, pseudo_type='Int')

def split(f, delimiter, pseudo_type):
    if delimiter.type == 'string' and (len(delimiter.value) == 1 or delimiter.value == '\\n'):
        return method_call(f, 'Split', [Node('char', value=delimiter.value, pseudo_type='Char')], ['List', 'String'])
    else:
        return method_call(f, 
            'Split', 
            [Node('array', elements=[delimiter]), attr(typename('StringSplitOptions', 'Library'), 'None', 'CSharpNone')], 
            pseudo_type=['List', 'String'])

def linq(name, z=True, swap=False):
    def x(l, f, *args):
        pseudo_type, args = args[-1], list(args[:-1])
        if args and swap:
            f, args[0] = args[0], f
        cs = method_call(l, name, [f] + args, pseudo_type)
        if z:
            cs.pseudo_type = 'CSharpEnumerable'
            return method_call(cs, 'ToList', [], pseudo_type)
        else:
            return cs
    return x

def pad(f, count, fill, pseudo_type):
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
    return method_call(
        method_call(
            receiver, 
            'Take', 
            
            [Node('binary_op', op='-', left=attr(receiver, 'Length', 'Int'), right=to_node(-to.value), pseudo_type='Int') if to.type == 'int' and to.value < 0 else to],
            pseudo_type=pseudo_type),
        'Drop', 
        [Node('binary_op', op='-', left=attr(receiver, 'Length', 'Int'), right=to_node(-from_.value), pseudo_type='Int') if from_.type == 'int' and from_.value < 0 else from_],
        pseudo_type=pseudo_type)

class Display(NormalLeakingNode):
    def as_expression(self):
        return [Node('static_call',
                    receiver=typename('Console', 'Library'),
                    message='WriteLine',
                    args=[arg],
                    pseudo_type='Void')
                for arg
                in self.args], None


def empty(l, _):
    return Node('unary_op', 
        op='not', 
        pseudo_type='Boolean', value=method_call(l, 'Any', [], 'Boolean'))