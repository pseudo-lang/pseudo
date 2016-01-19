from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class PythonTranslator(ApiTranslator):
    '''Python api translator'''

    api = {
        'List': {
            'push':         '#append',
            'pop':          '#pop',
            'length':       'Global.len'
        },
        'Dictionary': {
            'length':       'Global.len'
        }
    }
