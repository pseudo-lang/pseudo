from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class JSTranslator(ApiTranslator):

    api = {
        'List': {
            'push': '#push',
            'pop': '#pop',
            '.length': '#length'
        },
        'Dictionary': {
            '.length': '#length'
        }
    }
