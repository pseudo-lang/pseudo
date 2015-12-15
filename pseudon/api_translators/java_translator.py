from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class JavaTranslator(ApiTranslator):

    api = {
        'List': {
            'add': {
                (-1, t, [t]): '#push',
                (Int, t, [1]): '#insert',
            },
            'remove': {
                (-1, [t]): '#pop',
                (Int, [t]): '#remove'
            },
            'size': '#length'
        },
        'Dictionary': {
            'size': '#length'
        }
    }
