from pseudon.types import *
from pseudon.api_translator import ApiTranslator


class PythonTranslator(ApiTranslator):

    api = {
        'List': {
            'append': 		'#push',
            'pop': 	  		'#pop',
            '__len__': 		'#length'
        },
        'Dictionary': {
            '__len__': 		'#length'
        }
    }
