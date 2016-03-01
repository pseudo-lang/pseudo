from pseudon.types import *
from pseudon.api_translator import ApiTranslator
from pseudon.pseudon_tree import Node, method_call, call


class JSTranslator(ApiTranslator):
    '''Javascript api translator'''

    api = {
        'List': {
            '@equivalent':  'Array',

            'push':         '#push',
            'pop':          '#pop',
            'length':       '.length',
            'insert':       '.splice(%0, 0, %1)',
            'remove_at':    lambda receiver, index: method_call(receiver, 'splice', [index, Node('int', index.value + 1)]),
            'remove':       lambda receiver, index, value: method_call(
                            receiver, 'splice', [method_call(receiver, 'indexOf', [index]), value])
        },
        'Dictionary': {
            'length':       '.length',
            'keys':         'Object.keys',
            'values':       'Object.values'
        },
        'Enumerable': {
            'map':          '_.map',
            'filter':       '_.select',
            'reduce':       '_.reduce'
        }
    }

    dependencies = {
        'Enumerable': {
            '@all':         'lodash'
        }
    }
