from pseudo.pseudo_tree import Node, call, method_call, local, assignment, attr, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode

def expand_push(receiver, element):
        return Node(
            'assignment',
            target=receiver,
            value=call('append', [receiver, element]))

def expand_insert(receiver, index, element):
    return call('append', [])

def expand_map(receiver, function, assignment, pseudo_type):
    if function.type == 'lambda':
        iter = function.args[0]
    else:
        iter = 'element'
    return Node('block', block=[Node('_go_multi_assignment',
        name=local('result'),
        value=Node('_go_make_slice',
            type=receiver.pseudo_type,
            length=call('len', receiver))),
        for_each_with_index_statement(
            [iter, 'j'],
            receiver, [
                item_assignment(local('result'),
                    local('j'),
                    call(function, [iter]))]),
        local('result')])

def expand_filter(receiver, test, assignment, pseudo_type):
    if function.type == 'lambda':
        iter = function.args[0]
    else:
        iter = 'element'
    return Node('block', block=[
        Node('_go_multi_assignment',
            name=local('result'),
            value=Node('_go_make_slice',
                type=receiver.pseudo_type,
                length=call('len', receiver))),
            for_each_with_index_statement(
                [iter, 'j'],
                receiver, [
                    if_statement(
                        call(test, [iter]), [
                            local_assignment(
                                local('result'),
                                call('append', [local('result'), local(iter)]))], None)
            ]),
        local('result')])


def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if to:
            if from_.type == 'int' and from_.value == 0:
                return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                return Node('_go_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            return Node('_go_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

class Read(BizarreLeakingNode):
    '''
    transform `io:read`
    '''
    
    def temp_name(self, target):
        return '_read_result'

    def as_expression(self):
        return [
        Node('_go_multi_assignment',
            targets=[local('reader', 'Reader'), local('err', 'Error')],
            values=[call(attr(local('bufio', 'GoLibrary'),
                    'NewReader', ['Function', 'IO', 'Reader']), 
                [attr(local('os', 'GoLibrary'), 'Stdin', 'IO')],
                pseudo_type='Reader')]),
            call(
                attr(local('reader', 'Reader'), 
                    'ReadString',
                    ['Function', 'String', 'String']),
                    [to_node('\\n')],
                    pseudo_type='String')], None

    def as_assignment(self, target):
        expression = self.as_expression()
        expression[1] = assignment(target, expression[1])
        return expression

