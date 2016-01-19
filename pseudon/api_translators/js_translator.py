from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class JSTranslator(ApiTranslator):
    '''Javascript api translator'''

    api = {
        'List': {
            'push':         '#push',
            'pop':          '#pop',
            'length':       '.length'
        },
        'Dictionary': {
            'length':       '.length',
            'keys':         'Object.keys',
            'values':       'Object.values'
        },
        'Enumerable': {
            'map':          '_.map',
            'filter':       '_.select'
        },

        'Int': {
            '+':            '#+'
        }
    }
