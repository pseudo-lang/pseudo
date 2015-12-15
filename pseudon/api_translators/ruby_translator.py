from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class RubyTranslator(ApiTranslator):

    api = {
        'List': {
            'push': 		'#push',
            'pop':  		'#pop',
            'length': 		'#length'
        },
        'Dict': {
            'length':	 	'#length'
        }
    }
