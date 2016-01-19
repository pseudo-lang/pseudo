from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class RubyTranslator(ApiTranslator):
    '''Ruby api translator'''

    api = {
        'List': {
            'push':         '#push',
            'pop':          '#pop',
            'length':       '#length'
        },
        'Dictionary': {
            'length':       '#length',
            'keys':         '#keys',
            'values':       '#values'
        },
        'Enumerable': {
            'map':          '#map',
            'filter':       '#select'
        },

        'Int': {
            '+':            '#+'
        }
    }
