from pseudon.pseudon_tree import Node, call, method_call, local, assignment, to_node
from pseudon.api_handlers import BizarreLeakingNode, NormalLeakingNode

def expand_map(receiver, func):
    if func.type == 'lambda':
        return Node(
            '_list_comp',
            sequence=receiver)
    else:
        return call('map', [func, receiver])

def expand_filter(receiver, func):
    if func.type == 'lambda':
        return Node(
            '_list_comp')
    else:
        return call('filter', [func, receiver])

def expand_set_slice(receiver, from_=None, to=None, value=None, pseudo_type=None):
    s = expand_slice(receiver, from_, to, pseudo_type)
    return assignment(s, value)

def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if to:
            if from_.type == 'int' and from_.value == 0:
                return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                return Node('_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            return Node('_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

class ReadFile(BizarreLeakingNode):
    '''
    transforms `io:read_file`

    `io:read_file(name)`
    to 
    `with open(name, 'r') as _f:
        <target>/_file_contents = f.read()`
    '''

    def temp_name(self, target):
        return '_file_contents'

    # assign : as_assignment 
    # block-level: as_expression
    # inside: as_assignment with temp_name as target
    def as_expression(self):
        return [Node(
            '_with', 
            call=call('open', [self.args[0], to_node('r')], 'File'),
            context='_f', 
            block=[method_call(local('_f', 'File'), 'read', [], 'String')],
            pseudo_type='Void')], None

    def as_assignment(self, target):
        expression = self.as_expression()[0][0]
        expression.block[0] = assignment(target, expression.block[0])
        return [expression]


class WriteFile(NormalLeakingNode):
    '''
    transforms `io:write_file`

    `io:write_file(name, stuff)`
    `with open(name, 'w') as _f:
        _f.write(stuff)`
    '''

    def as_expression(self):
        return [], Node(
            '_with',
            call=call('open', [self.args[0], to_node('w')], 'File'),
            context='_f',
            block=[method_call(local('_f', 'File'), 'write', [self.args[1]], 'Void')],
            pseudo_type='Void')
