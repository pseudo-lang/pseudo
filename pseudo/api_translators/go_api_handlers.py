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
class Contains(BizarreLeakingNode):
    '''
    transform `sequenc:contains?`
    '''
    def temp_name(self, target):
        return '_contains'

    def as_expression(self):
        return [
            Node('_go_multi_assignment',
                targets=[
                    local('_', self.args[0].pseudo_type[1]),
                    local(self.temp_name(''), pseudo_type='Boolean')
                ],
                values=[
                    Node('index',
                        sequence=self.args[0],
                        index=self.args[1],
                        pseudo_type='MaybeElement')
                ]),
            local(self.temp_name(''), pseudo_type='Boolean')], None

    def as_assignment(self, target):
        expression = self.as_expression()[0]
        expression[0].targets[1] = target
        expression[1] = target
        return expression
class DictItems(BizarreLeakingNode):
    def temp_name(self, target):
        if self.args[0].type in ['local', 'instance_variable', 'typename']:
            name = self.args[0].name
        elif self.args[0].type == 'attr':
            name = self.args[0].attr
        else:
            name = ''
        return '_%s_%s' % (name, self.field)

    def singular_name(self):
        return self.temp_name('')[:-1]

    def index(self):
        return local('%s_index' % self.temp_name('').rpartition('_')[0], 0)

    def as_expression(self):
        e = self.temp_name('')
        e_singular = self.singular_name()
        e_index = self.index()
        if self.field == 'keys':
            field_type = self.args[0].pseudo_type[1]
            first = local(e_singular, field_type)
            second = local('_', self.args[0].pseudo_type[2])
        else:
            field_type = self.args[0].pseudo_type[2]
            first = local('_', self.args[0].pseudo_type[1])
            second = local(e_singular, field_type)
        e = local(e, field_type)
        e_singular = local(e_singular, field_type)
        return [assignment(e, Node('_go_make_slice', slice_type=['List', field_type], length=call('len', [self.args[0]], 'Int'), pseudo_type=['List', field_type])),
            assignment(e_index, to_node(0)),
            Node('for_statement',
                sequences=Node('for_sequence_with_items',
                    sequence=self.args[0]),
                iterators=Node('for_iterator_with_items',
                    key=first,
                    value=second),
                block=[
                    assignment(
                        Node('index', sequence=e, index=e_index, pseudo_type=field_type),
                        e_singular),
                    Node('aug_assignment', op='+', target=e_index, value=to_node(1))]),
            e], None

        def as_assignment(self, target):
            e = self.as_expression()[0]
            e[3] = assignment(target, e)
            return e


class DictKeys(DictItems):
    field = 'keys'

class DictValues(DictItems):
    field = 'values'

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
        expression = self.as_expression()[0]
        expression[1] = assignment(target, expression[1])
        return expression

