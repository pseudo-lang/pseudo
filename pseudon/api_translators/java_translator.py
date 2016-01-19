from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class JavaTranslator(ApiTranslator):
    '''Java api translator'''

    api = {
        'List': {
            'add': {
                (-1, t, (t)): '#push',
                (Int, t, (t)): '#insert',
            },
            'remove': {
                (-1, (t)): '#pop',
                (Int, (t)): '#remove'
            },
            'size': '#length'
        },
        'Dictionary': {
            'size': '#length'
        }
    }
