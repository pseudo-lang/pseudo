from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class SwiftTranslator(ApiTranslator):
    '''Swift api translator'''

    api = {
        'List': {
            'append': '#push',
            'popLast': '#pop',
            '.count': '#length'
        },
        'Dictionary': {
            '.count': '#length'
        }
    }
