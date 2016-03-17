from pseudo.pseudo_tree import Node, call, method_call, local, assignment, attr, to_node
from pseudo.api_handlers import BizarreLeakingNode, NormalLeakingNode
from pseudo.tree_transformer import TreeTransformer

def expand_push(receiver, element):
        return Node(
            'assignment',
            target=receiver,
            value=call('append', [receiver, element]))

def expand_insert(receiver, index, element):
    return call('append', [])

def empty(s, _):
    return Node('binary_op',
                op='==',
                left=call('len', [s], 'Int'),
                right=to_node(0),
                pseudo_type='Boolean')

def present(s, _):
    return Node('binary_op',
                op='>',
                left=call('len', [s], 'Int'),
                right=to_node(0),
                pseudo_type='Boolean')    

class ExpandMap(BizarreLeakingNode):
    def temp_name(self, target):
        if isinstance(target, str):
            return target
        elif target.type in ['local', 'typename', 'instance_variable']:
            return target.name
        elif target and target.type == 'attr':
            return target.attr
        else:
            return self.default

    default = '_results'

    def as_expression(self, target=None):
        _index = local('_index', 'Int')
        name = self.temp_name(target or self.default)
        z = local(name, pseudo_type=['List', self.args[-1].pseudo_type[2]])
        z_arg = local('_value', z.pseudo_type[1])
        return [assignment(z, Node('_go_make_slice', slice_type=z.pseudo_type, length=call('len', [self.args[0]], 'Int'))),
                Node('for_statement',
                    sequences=Node('for_sequence_with_index',
                        sequence=self.args[0]),
                    iterators=Node('for_iterator_with_index',
                        index=_index,
                        iterator=self.args[1].params[0] if self.args[1].type == 'anonymous_function' else z_arg),
                    block=self.args[1].block[:-1] + [
                        assignment(Node('index', sequence=z, index=_index, pseudo_type=z.pseudo_type[1]),
                            self.args[1].block[-1].value)] if self.args[1].type == 'anonymous_function' else
                        assignment(Node('index', sequence=z, index=_index, pseudo_type=z.pseudo_type[1]),
                            call(self.args[1], z_arg, z.pseudo_type[1]))),
                z], None

    def as_assignment(self, target):
        return self.as_expression(target)[0][:-1]

expand_map = ExpandMap

class ExpandFilter(ExpandMap):
    def as_expression(self, target=None):
        _index = local('_index', 'Int')
        name = self.temp_name(target or self.default)
        z = local(name, pseudo_type=self.args[0].pseudo_type)
        if self.args[1].type == 'anonymous_function':
            block_test = self.args[1].block[-1].value
            initial = self.args[1].block[:-1]
            z_arg = self.args[1].params[0]
        else:
            z_arg = local('_value', z.pseudo_type[1])
            block_test = call(self.args[1], z_arg, 'Boolean')
            initial = []
        return [Node('_go_declaration', decl=name, decl_type=z.pseudo_type),
                Node('for_statement',
                    sequences=Node('for_sequence_with_index',
                        sequence=self.args[0]),
                    iterators=Node('for_iterator_with_index',
                        index=_index,
                        iterator=z_arg),
                    block=initial + [
                        Node('if_statement',
                            test=block_test,
                            block=[assignment(
                                z, call('append', [z, z_arg], z.pseudo_type))],
                            otherwise=None)]),
                z], None

expand_filter = ExpandFilter

class ExpandReduce(ExpandMap):
    default = 'accumulator'
    def as_expression(self, target=None):
        t = self.temp_name(target or 'accumulator')
        if self.args[1].type == 'anonymous_function':
            initial = self.args[1].block[:-1]
            element = self.args[1].params[1]
            if target is None:
                target = self.args[1].params[0]
            elif target.name != self.args[1].params[0].name:
                self.args[1].block = ReduceRewriter(self.args[1].params[0].name, target.name).transform(self.args[1].block)
                self.args[1].params[0] = target
            block_result = self.args[1].block[-1].value
        else:
            initial = []
            element = local('_element', self.args[0].pseudo_type[1])
            if target is None:
                target = local(t, self.args[1].pseudo_type[-1])
            block_result = call(self.args[1], [element, target], target.pseudo_type)
    
        return [assignment(target, self.args[2]),
                Node('for_statement',
                    sequences=Node('for_sequence',
                        sequence=self.args[0]),
                    iterators=Node('for_iterator',
                        iterator=element),
                    block=initial + [
                        assignment(target, block_result)
                    ]),
                    target], None


expand_reduce = ExpandReduce

def extract_name(s, default=None):
    return getattr(s, 'name', getattr(s, 'attr', default or 'x'))

class Find(ExpandMap):
    default = '_found'
    def as_expression(self, target=None):
        t = self.temp_name(target or self.default)
        element = '_%sElement' % extract_name(self.args[0], t)
        j = '_%sIndex' % extract_name(self.args[0], t)
        element = local(element, self.args[0].pseudo_type[1])
        j = local(j, 'Int')
        if target is None:
            target = local(t, 'Int')
        return [assignment(target, to_node(-1)),
                Node('for_statement',
                    sequences=Node('for_sequence_with_index',
                        sequence=self.args[0]),
                    iterators=Node('for_iterator_with_index',
                        index=j,
                        iterator=element),
                    block=[
                        Node('if_statement',
                            test=Node('comparison', 
                                op='==',
                                pseudo_type='Boolean',
                                left=element,
                                right=self.args[1]),
                            block=[assignment(target, j), Node('break_')],
                            otherwise=None)]),
                target], None
                

def expand_slice(receiver, from_=None, to=None, pseudo_type=None):
    if from_:
        if pseudo_type: #to
            if from_.type == 'int' and from_.value == 0:
                return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
            else:
                if from_.type == 'int' and from_.value < 0:
                    from_ = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-from_.value), pseudo_type='Int')
                if to.type == 'int' and to.value < 0:
                    to = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-to.value), pseudo_type='Int')

                return Node('_go_slice', sequence=receiver, from_=from_, to=to, pseudo_type=pseudo_type)
        else:
            pseudo_type = to
            return Node('_go_slice_from', sequence=receiver, from_=from_, pseudo_type=pseudo_type)
    elif to:
        if to.type == 'int' and to.value < 0:
            to = Node('binary_op', op='-', left=call('len', [receiver], 'Int'), right=to_node(-to.value), pseudo_type='Int')
        return Node('_go_slice_to', sequence=receiver, to=to, pseudo_type=pseudo_type)
    else:
        return None

class ListContains(ExpandMap):
    default = '_contains'

    def as_expression(self, target=None):
        t = self.temp_name(target or self.default)
        element = '_%sElement' % extract_name(self.args[0], t)
        element = local(element, self.args[0].pseudo_type[1])
        if target is None:
            target = local(t, 'Int')
        return [assignment(target, Node('boolean', value='false', pseudo_type='Boolean')),
                Node('for_statement',
                    sequences=Node('for_sequence',
                        sequence=self.args[0]),
                    iterators=Node('for_iterator',
                        iterator=element),
                    block=[
                        Node('if_statement',
                            test=Node('comparison', 
                                op='==',
                                pseudo_type='Boolean',
                                left=element,
                                right=self.args[1]),
                            block=[assignment(target, Node('boolean', value='true', pseudo_type='Boolean')), Node('break_')],
                            otherwise=None,
                            pseudo_type='Void')]),
                target], None
        

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
class Int(BizarreLeakingNode):
    count = 0

    def temp_name(self, _, i=True):
        if self.count:
            result = '_int%d' % self.count
        else:
            result = '_int' # if several in the same call
        if i:
            type(self).count += 1
        return result

    def as_expression(self):
        t = self.temp_name('', False)
        target = local(t, 'Int')
        return [Node('_go_multi_assignment',
            targets=[target, local('_', 'Error')],
            values=[Node('static_call', 
                receiver=local('strconv', 'Library'), 
                message='Atoi',
                args=[self.args[0]], 
                pseudo_type=['GoResultWithError', 'Int'])]),
            target], None

    def as_assignment(self, target):
        e = self.as_expression()[0]
        e[0].targets[0] = target
        return e[:1]

            

class ReduceRewriter(TreeTransformer):
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name

    def transform_local(self, node, *x):
        if node.name == self.old_name:
            node.name = self.new_name
        return node

class DictItems(BizarreLeakingNode):
    def temp_name(self, _):
        if self.args[0].type in ['local', 'instance_variable', 'typename']:
            name = self.args[0].name
        elif self.args[0].type == 'attr':
            name = self.args[0].attr
        else:
            name = ''
        return '_%s%s' % (name, self.field.title())

    def singular_name(self):
        return self.temp_name('')[:-1]

    def index(self):
        if self.args[0].type in ['local', 'instance_variable', 'typename']:
            name = self.args[0].name
        elif self.args[0].type == 'attr':
            name = self.args[0].attr
        else:
            name = ''
        
        return local('_%sIndex' % name, 'Int')

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

class ReadFile(BizarreLeakingNode):
    '''transforms io:read_file'''
    def temp_name(self, target):
        return '_contents'

    def as_expression(self):
        l = local(self.temp_name(''), 'String')
        return [Node('_go_multi_assignment',
            targets=[l, local('_', 'Error')],
            values=[Node('static_call',
                message='ReadFile',
                receiver=local('ioutil', 'Library'),
                args=self.args,
                pseudo_type='MaybeBytez')]), 
            call('string', [l], 'String')], None

    def as_assignment(self, target):
        e = self.as_expression()[0]
        e[1] = assignment(target, e[1])
        return e

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

