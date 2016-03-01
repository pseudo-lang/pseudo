from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call, if_statement, for_each_with_index_statement, item_assignment


class GolangTranslator(ApiTranslator):
    '''Go translator'''

    @staticmethod
    def expand_push(receiver, element):
        return Node(
            '_go_assignment',
            name=receiver,
            value=call('append', [receiver, element]))

    @staticmethod
    def expand_pop(receiver):
        return call('append', [])

    @staticmethod
    def expand_insert(receiver, index, element):
        return call('append', [])

    @staticmethod
    def expand_map(receiver, function, assignment):
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

    @staticmethod
    def expand_filter(receiver, test, assignment):
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
    api = {
        'List': {
            '@equivalent':  'slice',

            'push':         expand_push,
            'pop':          expand_pop,
            'length':       '.length',
            'insert':       expand_insert

        },
        'Dictionary': {
        },
        'Enumerable': {
            'map':          expand_map,
            'filter':       expand_filter
        }
    }
