from pseudon.pseudon_tree import Node, call, method_call, local, assignment
from pseudon.api_handlers import BizarreLeakingNode, NormalLeakingNode

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
    return Node('block', block=[Node('_go_assignment',
        name=local('result'),
        value=Node('_make_slice',
            type=receiver.pseudon_type,
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
        Node('_go_assignment',
            name=local('result'),
            value=Node('_make_slice',
                type=receiver.pseudon_type,
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
                return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                return Node('_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            return Node('_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        return Node('_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

def read(assignment, namespace, function, args):
    return [
        local_assignment('reader', call(attr(local('bufio'), 'NewReader'), [attr(local('os'), 'Stdin')])),

        assignment_updated(
            local_assignment(call(
                attr(local('reader'), 
                    'ReadString', 
                    ['\n'], 
                    pseudo_type=['Tuple', 'String', 'Error']))))
        ]

class ReadFile(BizarreLeakingNode):
    pass

class WriteFile(BizarreLeakingNode):
    pass


