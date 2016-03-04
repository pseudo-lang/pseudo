from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call, if_statement, for_each_with_index_statement, index_assignment, local_assignment, attr


class GolangTranslator(ApiTranslator):
    '''Go translator'''

    def expand_push(receiver, element):
        return Node(
            '_go_assignment',
            name=receiver,
            value=call('append', [receiver, element]))

    def expand_pop(receiver):
        return call('append', [])

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

    methods = {
        'List': {
            '@equivalent':  'slice',

            'push':         go_bizarre('append'),
            'pop':          lambda receiver, pseudo_type: bizarre(go_last(receiver)
                ,
            'length':       '.length',
            'insert':       expand_insert

        },
        'Dictionary': {
        },
        'Enumerable': {
            'map':          expand_map,
            'filter':       expand_filter
        },
        'String': {
            '@equivalent':  'str',
            'substr':       expand_slice,
            'substr_from':  expand_slice,
            'length':       'len',
            'substr_to':    lambda receiver, to, _: expand_slice(receiver, None, to, pseudo_type=pseudo_type),
            'find':         '#find',
            'count':        '#count',
            'partition':    '#partition',
            'split':        '#split',
            'trim':         '#strip',
            'format':       '#format',
            'concat':       to_op('+'),
            'c_format':     to_op('%')
        }
    }

    functions = {
        'regexp':  {
            'compile':      'regexp.Compile',
            'escape':       'regexp.QuoteMeta'
        },
        'io': {
            'display':      'fmt.Println',
            'read':         bizarre(
                translate=read,
                temp_name='_input'
            )
        }
    }


    dependencies = {
        'regexp': {
            '@all':     'regexp'
        }
    }
