from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


class GoTranslator(ApiTranslator):
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
        },

        'Int': {
        }
    }
